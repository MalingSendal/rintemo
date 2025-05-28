import json
import os
from datetime import datetime
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.cluster import KMeans

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
                "traits": ["curious", "friendly", "sometimes sarcastic", "edgy"],
                "quirks": [],
                "memory_embeddings": [],
                "memory_texts": [],
                "trait_scores": {}  # <== NEW
            }

    def save(self):
        with open(PERSONALITY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)

    def observe_interaction(self, user_message, bot_response):
        observation = f"User: {user_message}\nAI: {bot_response}"
        embedding = personality_model.encode(observation).tolist()

        self.data["memory_embeddings"].append(embedding)
        self.data["memory_texts"].append(observation)

        # Trait scoring logic
        text = bot_response.lower()
        trait_scores = self.data.get("trait_scores", {})

        def increase_trait(trait):
            trait_scores[trait] = trait_scores.get(trait, 0) + 1

        def decrease_trait(trait):
            trait_scores[trait] = max(trait_scores.get(trait, 0) - 1, 0)

        if "ugh" in text or "whatever" in text or "you think?" in text:
            increase_trait("sarcastic")
        else:
            decrease_trait("sarcastic")

        if "aww" in text or "yay" in text:
            increase_trait("enthusiastic")
        else:
            decrease_trait("enthusiastic")

        if "i guess" in text or "maybe" in text:
            increase_trait("agreeable")

        if "i hate" in text or "no way" in text:
            increase_trait("grumpy")

        self.data["trait_scores"] = trait_scores
        self._update_personality_traits()
        self.save()

        # Optionally analyze clusters every 10 observations
        if len(self.data["memory_texts"]) % 10 == 0:
            self.analyze_personality_clusters()

    def analyze_personality_clusters(self):
        # Only analyze if enough data is present
        if len(self.data["memory_embeddings"]) < 5:
            return  # Not enough data to cluster meaningfully

        try:
            k = 2  # Number of clusters can be adjusted or dynamic
            kmeans = KMeans(n_clusters=k, random_state=0)
            embeddings = np.array(self.data["memory_embeddings"])
            kmeans.fit(embeddings)
            cluster_texts = [[] for _ in range(k)]

            for idx, label in enumerate(kmeans.labels_):
                cluster_texts[label].append(self.data["memory_texts"][idx])

            # Analyze clusters to infer personality traits
            for i, cluster in enumerate(cluster_texts):
                combined = " ".join(cluster).lower()

                # Simple heuristic to assign traits based on words found
                if "sarcastic" in combined or "sure..." in combined or "whatever" in combined:
                    trait = f"has sarcastic tendencies (Cluster {i})"
                elif "thank you" in combined or "nice" in combined or "glad" in combined:
                    trait = f"generally polite (Cluster {i})"
                elif "hate" in combined or "annoying" in combined:
                    trait = f"sometimes grumpy (Cluster {i})"
                else:
                    trait = f"neutral or unreadable tone (Cluster {i})"

                if trait not in self.data["traits"]:
                    self.data["traits"].append(trait)

            self.save()
        except Exception as e:
            print(f"Error clustering personality memories: {e}")

    def evolve_from_facts(self, facts):
        # Example: evolve personality based on favorite movie containing "horror"
        if "favorite_movie" in facts:
            fav_movie = facts["favorite_movie"].lower()
            if "horror" in fav_movie or "conjuring" in fav_movie or "thriller" in fav_movie:
                if "enjoys dark themes" not in self.data["traits"]:
                    self.data["traits"].append("enjoys dark themes")
                    self.save()

        # Add more fact-based personality evolution rules here
        if "favorite_color" in facts:
            color = facts["favorite_color"].lower()
            if color == "purple" and "likes mysterious vibes" not in self.data["traits"]:
                self.data["traits"].append("likes mysterious vibes")
                self.save()

    def get_traits_and_quirks(self):
        traits = ", ".join(self.data["traits"]) if self.data["traits"] else "no notable traits"
        quirks = ", ".join(self.data["quirks"]) if self.data["quirks"] else "no notable quirks yet"
        return f"Traits: {traits}. Quirks: {quirks}."

    def save_personality_snapshot(self):
        # Optional: Save snapshot for versioning personality states
        snapshot_file = f"personality_snapshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(snapshot_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2)

    def _update_personality_traits(self):
        trait_scores = self.data.get("trait_scores", {})
        traits = set(self.data["traits"])

        for trait, score in trait_scores.items():
            if score >= 3 and trait not in traits:
                traits.add(trait)
            elif score == 0 and trait in traits:
                traits.remove(trait)

        self.data["traits"] = list(traits)
