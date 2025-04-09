"""
Preservr Data Visualizations - Followers and Following

Author: Shirley Chen
Description: This module analyzes follower and following user data and displays mutuals, users who you follow but
don't follow you back, and users that follow you that you don't follow back.
Input: followers_1.json, following.json
Output: txt file with the aforementioned information saved to the 'OUTPUT_FOLDER' directory
Date: 2025-03
"""
import os
import json
import sys

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

def analyze_follow_data(folder_path):
    """
    Locate files and analyze followers vs. following data.
    Save results to OUTPUT_FOLDER.
    """
    followers_file = find_file_in_subdirectories(folder_path, "followers_1.json")
    following_file = find_file_in_subdirectories(folder_path, "following.json")

    if not followers_file or not following_file:
        print("Error: One or both required JSON files not found.")
        return

    followers = load_usernames(followers_file, "Followers")
    following = load_usernames(following_file, "Following")

    followers_set = set(followers)
    following_set = set(following)

    mutuals = sorted(followers_set & following_set)
    fans = sorted(followers_set - following_set)
    not_following_back = sorted(following_set - followers_set)

    # Create OUTPUT_FOLDER if it doesn't exist
    output_folder = os.path.join(folder_path, "OUTPUT_FOLDER")
    os.makedirs(output_folder, exist_ok=True)

    output_file = os.path.join(output_folder, "follow_analysis.txt")

    with open(output_file, "w", encoding="utf-8") as out:
        out.write("Mutuals:\n")
        out.write("\n".join(mutuals) + "\n\n")
        out.write("People who follow me but I don’t follow back:\n")
        out.write("\n".join(fans) + "\n\n")
        out.write("People I follow but who don’t follow me back:\n")
        out.write("\n".join(not_following_back))

    print(f"\n✅ Analysis written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python followers_following.py <folder_path>")
        sys.exit(1)

    input_folder = sys.argv[1]
    analyze_follow_data(input_folder)
