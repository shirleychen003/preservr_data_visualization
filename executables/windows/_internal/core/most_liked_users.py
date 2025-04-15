"""
Preservr Data Visualizations - Most Liked Users
Author: Luca Carnegie
Description: This module visualizes the most liked users across both story likes and post likes.
             It generates a side-by-side bar chart showing the top 5 users based on combined likes.
Input: liked_posts.json and story_likes.json files from the Instagram data archive
Output: Bar chart visualization saved in the output folder
Date: 2025-04-16
"""

import json
import matplotlib.pyplot as plt
import pandas as pd
import sys
import os
from collections import Counter

def find_file_in_subdirectories(folder_path, filename):
    """
    Recursively search for the specified file in subdirectories.
    """
    for root, dirs, files in os.walk(folder_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

def load_story_likes_data(folder_path):
    """
    Load and parse story likes data from story_likes.json
    Returns a dictionary of usernames and their like counts
    """
    # Find story_likes.json file
    story_likes_path = find_file_in_subdirectories(folder_path, "story_likes.json")
    
    if story_likes_path is None:
        print(f"Warning: Could not find story_likes.json in {folder_path} or its subdirectories")
        return {}
    
    # Load and parse the JSON data
    try:
        with open(story_likes_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        # Extract story likes
        likes = [entry["title"] for entry in data.get("story_activities_story_likes", [])]
        
        # Count occurrences of each username
        return dict(Counter(likes))
    
    except Exception as e:
        print(f"Error loading story likes data: {e}")
        return {}

def load_post_likes_data(folder_path):
    """
    Load and parse post likes data from liked_posts.json
    Returns a dictionary of usernames and their like counts
    """
    # Find liked_posts.json file
    liked_posts_path = find_file_in_subdirectories(folder_path, "liked_posts.json")
    
    if liked_posts_path is None:
        print(f"Warning: Could not find liked_posts.json in {folder_path} or its subdirectories")
        return {}
    
    # Load and parse the JSON data
    try:
        with open(liked_posts_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        
        # Extract titles (media owners) from the data
        media_titles = []
        for item in data.get("likes_media_likes", []):
            title = item.get("title", "")
            if title and title != "Unknown":
                media_titles.append(title)
        
        # Count occurrences of each username
        return dict(Counter(media_titles))
    
    except Exception as e:
        print(f"Error loading post likes data: {e}")
        return {}

def combine_like_data(story_likes, post_likes):
    """
    Combine story likes and post likes data and find the top users by total likes
    Returns a DataFrame with columns for username, story likes, post likes, and total likes
    """
    # Get all unique usernames
    all_users = set(story_likes.keys()) | set(post_likes.keys())
    
    # Create lists for DataFrame
    usernames = []
    story_like_counts = []
    post_like_counts = []
    total_likes = []
    
    # Populate the lists
    for user in all_users:
        story_count = story_likes.get(user, 0)
        post_count = post_likes.get(user, 0)
        total = story_count + post_count
        
        usernames.append(user)
        story_like_counts.append(story_count)
        post_like_counts.append(post_count)
        total_likes.append(total)
    
    # Create DataFrame
    df = pd.DataFrame({
        "Username": usernames,
        "Story Likes": story_like_counts,
        "Post Likes": post_like_counts,
        "Total Likes": total_likes
    })
    
    # Sort by total likes in descending order
    df = df.sort_values(by="Total Likes", ascending=False)
    
    return df

def create_bar_chart(data, folder_path):
    """
    Create a side-by-side bar chart showing the top 5 users by total likes
    """
    # Get the top 5 users
    top_users = data.head(5)
    
    # Set up the figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Set width of bars
    bar_width = 0.35
    
    # Set positions of the bars on X axis
    positions1 = range(len(top_users))
    positions2 = [x + bar_width for x in positions1]
    
    # Create bars with blue and red colors as requested
    ax.bar(positions1, top_users["Story Likes"], width=bar_width, color='blue', label='Story Likes')
    ax.bar(positions2, top_users["Post Likes"], width=bar_width, color='red', label='Post Likes')
    
    # Add labels, title, and legend
    ax.set_xlabel('Users')
    ax.set_ylabel('Number of Likes')
    ax.set_title('Top 5 Users by Combined Likes')
    ax.set_xticks([r + bar_width/2 for r in range(len(top_users))])
    ax.set_xticklabels(top_users["Username"], rotation=45, ha='right')
    ax.legend()
    
    plt.tight_layout()
    
    # Define the output path inside OUTPUT_FOLDER
    output_folder = os.path.join(folder_path, "OUTPUT_FOLDER")
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, "most_liked_users_barchart.png")
    
    # Save as PNG
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Visualization saved to: {output_path}")
    plt.close()

def process_likes_data(folder_path):
    """
    Main function to process likes data and generate visualization
    """
    # Load data
    story_likes = load_story_likes_data(folder_path)
    post_likes = load_post_likes_data(folder_path)
    
    # Check if we have any data
    if not story_likes and not post_likes:
        print("Error: No data found in either story_likes.json or liked_posts.json")
        return False
    
    # Combine data and create visualization
    combined_data = combine_like_data(story_likes, post_likes)
    create_bar_chart(combined_data, folder_path)
    
    return True

def main():
    """
    Entry point for the script
    """
    if len(sys.argv) < 2:
        print("Usage: python most_liked_users.py <folder_path>")
        sys.exit(1)

    folder = sys.argv[1]
    process_likes_data(folder)

if __name__ == "__main__":
    main()
