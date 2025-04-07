import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Load the JSON file
with open("../test_data/recommended_topics.json", "r", encoding="utf-8") as file:
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
wc = WordCloud(width=800, height=500, background_color="white").generate(text)

output_path = "../images/wordcloud_topics.png"

# Print the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.show()

# Save the visualization
plt.figure(figsize=(10, 5))
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")

# Save as PNG
plt.savefig(output_path, dpi=300, bbox_inches="tight")
print(f"Visualization saved to: {output_path}")

plt.show()