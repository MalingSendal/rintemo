# app/personality.py

import json
import os
from sentence_transformers import SentenceTransformer
import numpy as np

PERSONALITY_FILE = "personality.json"
personality_model = SentenceTransformer('all-MiniLM-L6-v2')

class Personality:
    def __init__(self):
        self.data = self.load_personality()

    def load_personality(self):
        if os.path.exists(PERSONALITY_FILE):
            with open(PERSONALITY_FILE, 'r') as f:
                return json.load(f)
        else:
            return {
                "traits": ["curious", "friendly", "sometimes sarcastic"],
                "quirks": [],
                "memory_embeddings": [],
                "memory_texts": []
            }

    def save(self):
        with open(PERSONALITY_FILE, 'w') as f:
            json.dump(self.data, f, indent=2)

    def observe_interaction(self, user_message, bot_response):
        observation = f"User: {user_message}\nAI: {bot_response}"
        embedding = personality_model.encode(observation).tolist()
        
        self.data["memory_embeddings"].append(embedding)
        self.data["memory_texts"].append(observation)
        
        # Simple quirk generation: detect specific words or tone
        if "huh" in bot_response or "weird" in bot_response:
            if "says 'huh' often" not in self.data["quirks"]:
                self.data["quirks"].append("says 'huh' often")

        # Save every time we observe
        self.save()

    def get_traits_and_quirks(self):
        traits = ", ".join(self.data["traits"])
        quirks = ", ".join(self.data["quirks"]) if self.data["quirks"] else "no notable quirks yet"
        return f"Traits: {traits}. Quirks: {quirks}."
