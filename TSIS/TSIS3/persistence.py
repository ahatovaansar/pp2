import json

def load_leaderboard():
    try:
        with open("leaderboard.json") as f:
            return json.load(f)
    except:
        return []

def save_leaderboard(data):
    with open("leaderboard.json", "w") as f:
        json.dump(data, f, indent=4)