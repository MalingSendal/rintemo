#routes.py

from datetime import datetime
from flask import request, jsonify, render_template, send_file
from .memory import LongTermMemory
from .facts import FactMemory
from .llm_client import call_llm
from .config import Config
from .personality import Personality
from gtts import gTTS
import json
import pytz
import csv
import os
import re
# import uuid
# voice_file = f"response_{uuid.uuid4().hex}.mp3" <== for unique voice file names


SONGS_FOLDER = "songs"  # Folder where songs are stored

def calculate_time_difference(last_interaction):
    jakarta_tz = pytz.timezone("Asia/Jakarta")
    now = datetime.now(jakarta_tz)

    if not last_interaction:
        return "This is our first interaction!"
    last_time = datetime.strptime(last_interaction, "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    delta = now - last_time
    if delta.days > 0:
        return f"It's been {delta.days} day(s) since we last talked."
    elif delta.seconds > 3600:
        return f"It's been {delta.seconds // 3600} hour(s) since we last talked."
    elif delta.seconds > 60:
        return f"It's been {delta.seconds // 60} minute(s) since we last talked."
    else:
        return "We just talked a moment ago!"
    
def generate_voice_response(text, personality_traits=None):
    """Generate a voice response using gTTS."""
    try:
        # Generate speech using gTTS
        tts = gTTS(text=text, lang='en', slow=False)  # Default voice is female
        voice_file = 'response.mp3'
        tts.save(voice_file)  # Save the audio file
        return voice_file
    except Exception as e:
        raise RuntimeError(f"Error generating voice response: {str(e)}")

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
        user_id = request.form.get("user_id")
        user_reference = request.form.get("user_reference")
        user_input = request.form.get("message")

        if not user_input:
            return jsonify({"error": "No message provided"}), 400
        
        try:
            # Detect if the user is asking to play a song
            song_request_match = re.search(r"play(?: the)? (.+?) song", user_input, re.IGNORECASE)
            if song_request_match:
                song_name = song_request_match.group(1).strip()
                song_path = os.path.join(SONGS_FOLDER, f"{song_name}.mp3")

                if os.path.exists(song_path):
                    # Generate a voice response announcing the song
                    announcement = f"Now playing {song_name}."
                    voice_file = generate_voice_response(announcement)

                    return jsonify({
                        "response": announcement,
                        "voice_file": voice_file,
                        "song_file": song_path
                    })
                else:
                    # Respond if the song is not found
                    not_found_message = f"Sorry, I couldn't find the song '{song_name}'."
                    voice_file = generate_voice_response(not_found_message)

                    return jsonify({
                        "response": not_found_message,
                        "voice_file": voice_file
                    })

            # Retrieve last interaction time
            last_interaction = LongTermMemory.get_last_interaction_time(user_id)
            time_message = calculate_time_difference(last_interaction)
            LongTermMemory.update_last_interaction_time(user_id)

            # Retrieve user-specific facts
            user_facts = FactMemory.get_user_facts(user_id)
            if user_facts:
                facts_text = ", ".join(f"{k.replace('_', ' ')}: {v}" for k, v in user_facts.items())
            else:
                facts_text = f"I don't know much about {user_reference} yet."

            if not user_facts:
                user_reference = request.form.get("user_reference", "Unknown User")
            else:
                user_reference = user_facts.get("user_name", request.form.get("user_reference", "Unknown User"))

            # Prepare system messages
            messages = [{"role": "system", "content": Config.get_system_prompt()}]
            messages.append({"role": "system", "content": f"Facts about {user_reference}: {facts_text}"})

            # Extract and save user-specific facts
            new_facts = FactMemory.extract_facts_from_message(user_input)
            for key, value in new_facts.items():
                FactMemory.save_user_fact(user_id, key, value)  # Correct method

            # Add facts to system messages
            messages.append({"role": "system", "content": f"Facts about {user_reference}: {facts_text}"})

            # Personality and memory handling
            personality = Personality(user_id)
            recalled_memories = LongTermMemory.recall_memories(user_input)
            personality.evolve_from_facts(new_facts)

            personality_context = personality.get_traits_and_quirks()
            messages.append({
                "role": "system",
                "content": f"Here are your current behavioral tendencies and quirks: {personality_context}. "
                        "Maintain consistency with your evolving traits."
            })

            for memory in recalled_memories:
                messages.append({"role": "system", "content": memory})

            # Add user input and get bot response
            messages.append({"role": "user", "content": user_input})
            bot_response = call_llm(messages)

            # Save memory and observe interaction
            LongTermMemory.save_memory(user_id, user_input, bot_response)
            personality.observe_interaction(user_input, bot_response)

            # Retrieve personality traits
            personality = Personality(user_id)
            personality_traits = personality.data.get("traits", [])

            # Generate voice response with dynamic adjustments
            voice_file = generate_voice_response(bot_response, personality_traits)

            return jsonify({
                "response": bot_response,
                "voice_file": voice_file,  # Return the voice file path
                "memories_used": recalled_memories
            })

        except Exception as e:
            app.logger.error(f"Chat error: {str(e)}")
            return jsonify({"error": "Internal server error", "details": str(e)}), 500

    @app.route("/play_song", methods=["POST"])
    def play_song():
        song_name = request.form.get("song_name")
        if not song_name:
            return jsonify({"error": "No song name provided"}), 400

        # Check if the song exists in the folder
        song_path = os.path.join(SONGS_FOLDER, f"{song_name}.mp3")
        if not os.path.exists(song_path):
            return jsonify({"error": f"Song '{song_name}' not found"}), 404

        try:
            # Generate a voice response announcing the song
            announcement = f"Now playing {song_name}."
            voice_file = generate_voice_response(announcement)

            # Return the voice file and the song file
            return jsonify({
                "announcement_voice_file": voice_file,
                "song_file": song_path
            })
        except Exception as e:
            app.logger.error(f"Error playing song: {str(e)}")
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
        
