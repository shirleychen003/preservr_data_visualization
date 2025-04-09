import os
import json

# File paths
FOLLOWERS_FILE = "../test_data/followers_1.json"
FOLLOWING_FILE = "../test_data/following.json"
OUTPUT_FILE = "../test_data/follow_analysis.txt"

def load_usernames(filepath, label):
    """
    Load usernames from Instagram JSON file. Supports top-level lists and nested keys.
    """
    usernames = []
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

            # If data is a dict with a key like "relationships_following"
            if isinstance(data, dict) and "relationships_following" in data:
                data = data["relationships_following"]

            for entry in data:
                if "string_list_data" in entry and entry["string_list_data"]:
                    username = entry["string_list_data"][0]["value"].strip()
                    usernames.append(username)

            print(f"[{label}] Loaded {len(usernames)} usernames from {filepath}")

    except Exception as e:
        print(f"Error loading {label}: {e}")
    return usernames


def analyze_follow_data():
    followers = load_usernames(FOLLOWERS_FILE, "Followers")
    following = load_usernames(FOLLOWING_FILE, "Following")

    followers_set = set(followers)
    following_set = set(following)

    print(f"\nSet Sizes:")
    print(f"- Followers: {len(followers_set)}")
    print(f"- Following: {len(following_set)}")

    # Show some sample values
    print(f"\nSample followers: {followers[:5]}")
    print(f"Sample following: {following[:5]}")

    mutuals = sorted(followers_set & following_set)
    fans = sorted(followers_set - following_set)
    not_following_back = sorted(following_set - followers_set)

    print(f"\n🔁 Found {len(mutuals)} mutuals.")
    print(f"👀 Fans (they follow you, you don’t follow back): {len(fans)}")
    print(f"🚫 Not following back (you follow them, they don’t follow you): {len(not_following_back)}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("Mutuals:\n")
        out.write("\n".join(mutuals) + "\n\n")
        out.write("People who follow me but I don’t follow back:\n")
        out.write("\n".join(fans) + "\n\n")
        out.write("People I follow but who don’t follow me back:\n")
        out.write("\n".join(not_following_back))

    print(f"\n✅ Analysis written to {OUTPUT_FILE}")

if __name__ == "__main__":
    analyze_follow_data()
