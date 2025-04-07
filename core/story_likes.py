'''
Preservr Data Visualizations - Story Likes
Author: Shirley Chen
Description: This module provides visualization tools for analyzing and displaying
             story likes data for the Preservr project. It processes story likes datasets
             and generates a word cloud to visualize which users had interacted most with
             the user's stories
Input: Liked posts data files stored in the 'data' directory
Output: Visualization files saved to the 'output' directory
Date: 2025-03
'''

import json
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

# Load JSON file
with open("../preservr_data_visualization/test_data/story_likes.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract story likes
likes = [entry["title"] for entry in data.get("story_activities_story_likes", [])]

# Count occurrences of each user
like_counts = Counter(likes)

# Find the most active liker
most_active_liker, max_likes = like_counts.most_common(1)[0]

# Sort users by like count for better visualization
sorted_likes = dict(sorted(like_counts.items(), key=lambda x: x[1], reverse=True))

# Plot Word Cloud
wc = WordCloud(width=800, height=500, background_color="white", colormap="coolwarm")
wc.generate_from_frequencies(like_counts)

plt.figure(figsize=(10, 5))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.title(f"Frequent Story Likers (Top: {most_active_liker} - {max_likes} likes)")

output_path = "../preservr_data_visualization/images/story_likes_visualization.png"

# Save the visualization
plt.figure(figsize=(10, 5))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.title(f"Frequent Story Likers (Top: {most_active_liker} - {max_likes} likes)")

# Save as PNG
plt.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"Visualization saved to: {output_path}")