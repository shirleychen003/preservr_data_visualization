import os
import sys
import json
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def generate_topic_wordcloud(folder_path):
    """
    Generate a word cloud from recommended topics in the given folder.
    """
    # Construct full paths for input and output
    topics_path = os.path.join(folder_path, "recommended_topics.json")
    output_path = os.path.join(folder_path, "top_topics.png")

    # Load the JSON file
    with open(topics_path, "r", encoding="utf-8") as file:
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

    # Print and save the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")

    # Save as PNG
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Visualization saved to: {output_path}")

# Entry point for command-line use
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python recommended_topics.py <folder_path>")
        sys.exit(1)

    folder = sys.argv[1]
    generate_topic_wordcloud(folder)
