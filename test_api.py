import os
from dotenv import load_dotenv
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

print(f"Loaded Discord Token: {DISCORD_TOKEN}")
