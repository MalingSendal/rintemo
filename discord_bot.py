import discord
import os
import requests
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

    # Only respond if message starts with "!rin"
    if not user_input.lower().startswith("!rin"):
        return

    # Remove the "!rin" prefix before sending to the Flask backend
    user_input = user_input[len("!rin"):].strip()

    try:
        # Send to Flask backend
        response = requests.post(FLASK_BACKEND_URL, data={"message": user_input})
        response.raise_for_status()

        json_data = response.json()
        bot_reply = json_data.get("response", "Sorry, I had no response.")

    except Exception as e:
        bot_reply = f"⚠️ Error: {str(e)}"

    await message.channel.send(bot_reply)

client.run(DISCORD_TOKEN)
