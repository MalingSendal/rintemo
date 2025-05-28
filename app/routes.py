#routes.py

from flask import request, jsonify, render_template
from .memory import LongTermMemory
from .facts import FactMemory
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
            # Extract and save new facts
            new_facts = FactMemory.extract_facts_from_message(user_input)
            for key, value in new_facts.items():
                FactMemory.save_fact(key, value)

            # Step 1: Initialize personality
            personality = Personality()

            # Step 2: Recall relevant memories
            recalled_memories = LongTermMemory.recall_memories(user_input)

            # Step 3: Evolve personality from facts dynamically
            personality.evolve_from_facts(new_facts)

            # Step 4: Build message list
            messages = [{"role": "system", "content": Config.get_system_prompt()}]

            # Add fact summary into the system prompt
            facts = FactMemory.get_all_facts()
            if facts:
                facts_text = ", ".join(f"{k.replace('_', ' ')}: {v}" for k, v in facts.items())
                messages.append({"role": "system", "content": f"Facts about the user: {facts_text}"})

            # Step 5: Inject personality context (traits and quirks)
            personality_context = personality.get_traits_and_quirks()
            messages.append({
                "role": "system",
                "content": f"Here are your current behavioral tendencies and quirks: {personality_context}. "
                        "Maintain consistency with your evolving traits."
            })

            # Step 6: Add recalled memories as system messages
            for memory in recalled_memories:
                messages.append({"role": "system", "content": memory})

            # Step 7: Add user message
            messages.append({"role": "user", "content": user_input})

            # Step 8: Call the LLM
            bot_response = call_llm(messages)

            # Step 9: Save to long-term memory
            LongTermMemory.save_memory(user_id, user_input, bot_response)

            # Step 10: Let personality module observe interaction
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
