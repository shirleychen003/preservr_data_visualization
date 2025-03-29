import json
import matplotlib.pyplot as plt
from collections import Counter

# Load JSON file
with open("story_likes.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract story likes
likes = [entry["title"] for entry in data.get("story_activities_story_likes", [])]

# Count occurrences of each user
like_counts = Counter(likes)

# Find the most active liker
most_active_liker, max_likes = like_counts.most_common(1)[0]

# Sort users by like count for better visualization
sorted_likes = dict(sorted(like_counts.items(), key=lambda x: x[1], reverse=True))

# Plot the data
plt.figure(figsize=(10, 5))
plt.bar(range(len(sorted_likes)), sorted_likes.values(), color="skyblue")  # Use index instead of names
plt.xlabel("Users")  # Generic label
plt.ylabel("Number of Story Likes")
plt.title(f"Story Likes per User (Most Active: {most_active_liker} - {max_likes} likes)")
plt.xticks([])  # Hides x-axis labels
plt.tight_layout()

# Show the plot
plt.show()

