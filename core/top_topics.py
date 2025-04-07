import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load the JSON file
with open("../recommended_topics.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract topic names
topics = [
    item["string_map_data"]["Name"]["value"]
    for item in data.get("topics_your_topics", [])
    if "Name" in item.get("string_map_data", {})
]

# Join topics into a single string for word cloud generation
text = " ".join(topics)

# Generate word cloud
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

# Print the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()