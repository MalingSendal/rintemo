# facts.py

import json
import re
import os

FACTS_FILE = "user_facts.json"

class FactMemory:
    @staticmethod
    def load_facts():
        if os.path.exists(FACTS_FILE):
            with open(FACTS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    @staticmethod
    def save_fact(key, value):
        facts = FactMemory.load_facts()
        facts[key] = value
        with open(FACTS_FILE, "w", encoding="utf-8") as f:
            json.dump(facts, f, indent=2)

    @staticmethod
    def get_all_facts():
        return FactMemory.load_facts()

    @staticmethod
    def extract_facts_from_message(message):
        # Simple fact patterns like "My favorite color is purple"
        patterns = [
            (r"\bmy name is ([\w\s]+)", "user_name"),
            (r"\bi am ([\w\s]+)", "user_identity"),
            (r"\bfavorite color is (\w+)", "favorite_color"),
            (r"\bi like ([\w\s]+)", "likes"),
            (r"\bi love ([\w\s]+)", "loves"),
            (r"\bi hate ([\w\s]+)", "hates"),
            (r"\bi enjoy ([\w\s]+)", "enjoys"),
            (r"\bi prefer ([\w\s]+)", "preference"),
            (r"\bi live in ([\w\s]+)", "location"),
            (r"\bi was born in ([\w\s]+)", "birthplace"),
            (r"\bi work as a[n]? ([\w\s]+)", "occupation"),
            (r"\bi (have|own) a[n]? ([\w\s]+)", "ownership"),
            (r"\bmy birthday is (.+)", "birthday"),
            (r"\bi speak ([\w\s]+)", "languages"),
            (r"\bi use ([\w\s]+)", "tools_or_platforms"),
            (r"\bmy favorite food is ([\w\s]+)", "favorite_food"),
            (r"\bmy favorite movie is ([\w\s]+)", "favorite_movie"),
            (r"\bmy favorite book is ([\w\s]+)", "favorite_book"),
            (r"\bmy favorite song is ([\w\s]+)", "favorite_song"),
            (r"\bi am from ([\w\s]+)", "hometown"),
            (r"\bi study ([\w\s]+)", "field_of_study"),
            (r"\bi'm studying ([\w\s]+)", "field_of_study"),
            (r"\bi'm a ([\w\s]+)", "user_identity"),
        ]

        found_facts = {}
        for pattern, key in patterns:
            match = re.search(pattern, message.lower())
            if match:
                found_facts[key] = match.group(1).strip()
        return found_facts
