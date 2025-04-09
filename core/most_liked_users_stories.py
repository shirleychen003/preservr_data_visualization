"""
Instagram Follow Data Analyzer
Author: Shirlye Chen
Description: This script compares a user's Instagram followers and followings
             using JSON files exported from Instagram. It identifies mutuals,
             fans (followers not followed back), and people not following back.
Input: followers_1.json and following.json located in subdirectories under a given folder.
Output: follow_analysis.txt written to the same folder as the data.
Date: 2025-04
"""

import os
import sys
import json

def find_file_in_subdirectories(folder_path, filename):
    """
    Recursively search for the specified file in subdirectories.
    """
    for root, dirs, files in os.walk(folder_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

def load_usernames(filepath, label):
    """
    Load usernames from Instagram JSON file. Supports top-level lists and nested keys.
    """
    usernames = []
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

            # Handle nested structure in following.json
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

def analyze_follow_data(base_folder):
    """
    Compare followers and following data, write mutuals, fans, and non-followers to file.
    """
    followers_path = find_file_in_subdirectories(base_folder, "followers_1.json")
    following_path = find_file_in_subdirectories(base_folder, "following.json")

    if not followers_path or not following_path:
        print("❌ Error: Required files not found in subdirectories.")
        return

    followers = load_usernames(followers_path, "Followers")
    following = load_usernames(following_path, "Following")

    followers_set = set(followers)
    following_set = set(following)

    print(f"\nSet Sizes:")
    print(f"- Followers: {len(followers_set)}")
    print(f"- Following: {len(following_set)}")

    mutuals = sorted(followers_set & following_set)
    fans = sorted(followers_set - following_set)
    not_following_back = sorted(following_set - followers_set)

    print(f"\n🔁 Mutuals: {len(mutuals)}")
    print(f"👀 Fans (follow you, not followed back): {len(fans)}")
    print(f"🚫 Not following back (you follow, they don't): {len(not_following_back)}")

    output_path = os.path.join(base_folder, "follow_analysis.txt")
    with open(output_path, "w", encoding="utf-8") as out:
        out.write("🔁 Mutuals:\n")
        out.write("\n".join(mutuals) + "\n\n")

        out.write("👀 Fans (follow you, not followed back):\n")
        out.write("\n".join(fans) + "\n\n")

        out.write("🚫 Not following back (you follow, they don't):\n")
        out.write("\n".join(not_following_back))

    print(f"\n✅ Analysis written to {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python follow_data_analyzer.py <folder_path>")
        sys.exit(1)

    base_folder = sys.argv[1]
    analyze_follow_data(base_folder)
