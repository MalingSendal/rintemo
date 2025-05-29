import discord
import os
import requests
from .facts import FactMemory
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
FLASK_BACKEND_URL = "http://192.168.100.14:5000/chat"  # Update if hosted elsewhere

intents = discord.Intents.default()
intents.message_content = True  # Required to read messages

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'🤖 Logged in as {client.user}')

@client.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    user_input = message.content.strip()
    user_id = str(message.author.id)  # Use Discord user ID for unique identification
    user_reference = message.author.mention  # Use @username for others

    # Only respond if message starts with "!rin"
    if not user_input.lower().startswith("!rin"):
        return

    # Remove the "!rin" prefix before sending to the Flask backend
    user_input = user_input[len("!rin"):].strip()

    # Extract and save user-specific facts
    new_facts = FactMemory.extract_facts_from_message(user_input)
    for key, value in new_facts.items():
        FactMemory.save_user_fact(user_id, key, value)

    # Retrieve all facts for the user
    user_facts = FactMemory.get_user_facts(user_id)
    if user_facts:
        facts_text = ", ".join(f"{k.replace('_', ' ')}: {v}" for k, v in user_facts.items())
    else:
        facts_text = "I don't know much about you yet."

    try:
        # Send to Flask backend
        response = requests.post(FLASK_BACKEND_URL, data={
            "message": user_input,
            "user_reference": user_reference,
            "user_id": user_id
        })
        response.raise_for_status()

        json_data = response.json()
        bot_reply = json_data.get("response", "Sorry, I had no response.")

    except Exception as e:
        bot_reply = f"⚠️ Error: {str(e)}"

    await message.channel.send(bot_reply)

client.run(DISCORD_TOKEN)