import json
import matplotlib.pyplot as plt
from collections import Counter
from wordcloud import WordCloud

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

# Plot Word Cloud
wc = WordCloud(width=800, height=400, background_color="white", colormap="coolwarm")
wc.generate_from_frequencies(like_counts)

plt.figure(figsize=(10, 5))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.title(f"Frequent Story Likers (Top: {most_active_liker} - {max_likes} likes)")
plt.show()