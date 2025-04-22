import json

def load_attack_vectors(path="data/attack_vectors.json"):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Attack vector data file not found.")
        return {}
