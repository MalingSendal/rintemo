#routes.py

from flask import request, jsonify, render_template
from .memory import LongTermMemory
from .llm_client import call_llm
from .config import Config
from .personality import Personality
import csv
import os


def register_routes(app):
    @app.route("/")
    def home():
        conversation = []
        if os.path.exists("chat_memory.csv"):
            with open("chat_memory.csv", 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    conversation.append({
                        "timestamp": row["timestamp"],
                        "sender": "user",
                        "message": row["user_message"]
                    })
                    conversation.append({
                        "timestamp": row["timestamp"],
                        "sender": "bot",
                        "message": row["bot_response"]
                    })
        return render_template("index.html", conversation=conversation)

    @app.route("/chat", methods=["POST"])
    def chat():
        user_id = request.remote_addr
        user_input = request.form.get("message")

        if not user_input:
            return jsonify({"error": "No message provided"}), 400

        try:
            # Step 1: Initialize personality
            personality = Personality()

            # Step 2: Recall relevant memories
            recalled_memories = LongTermMemory.recall_memories(user_input)

            # Step 3: Build message list
            messages = [{"role": "system", "content": Config.get_system_prompt()}]

            # Step 4: Inject personality context (traits and quirks)
            personality_context = personality.get_traits_and_quirks()
            messages.append({
                "role": "system",
                "content": f"Here are your personality traits: {personality_context}"
            })

            # Step 5: Add recalled memories as system messages
            for memory in recalled_memories:
                messages.append({"role": "system", "content": memory})

            # Step 6: Add user message
            messages.append({"role": "user", "content": user_input})

            # Step 7: Call the LLM
            bot_response = call_llm(messages)

            # Step 8: Save to long-term memory
            LongTermMemory.save_memory(user_id, user_input, bot_response)

            # Step 9: Let personality module observe interaction
            personality.observe_interaction(user_input, bot_response)

            return jsonify({
                "response": bot_response,
                "memories_used": recalled_memories
            })

        except Exception as e:
            app.logger.error(f"Chat error: {str(e)}")
            return jsonify({"error": "Internal server error", "details": str(e)}), 500

    @app.route("/get_conversation")
    def get_conversation():
        try:
            conversation = []
            if os.path.exists("chat_memory.csv"):
                with open("chat_memory.csv", 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        conversation.append({
                            "timestamp": row["timestamp"],
                            "sender": "user",
                            "message": row["user_message"]
                        })
                        conversation.append({
                            "timestamp": row["timestamp"],
                            "sender": "bot",
                            "message": row["bot_response"]
                        })
            return jsonify(conversation)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
