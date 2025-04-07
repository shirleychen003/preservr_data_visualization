'''
Preservr Data Visualizations
Author: Luca Carnegie
Description: This module provides visualization tools for analyzing and displaying
             comment data for the Preservr project. It processes comment datasets
             and generates a word cloud to visualize the most commented media owners by
             the user.
Input: Comment data files stored in the 'data' directory
Output: Visualization files saved to the 'output' directory
Date: 2023-11-21
'''

import json
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os
import sys

def most_commented_barchart(owner_counts, output_path):
    """
    Create a bar chart showing the number of comments per user.
    
    Args:
        owner_counts (DataFrame): DataFrame containing media owners and comment counts
        output_path (str): Path to save the visualization
    """
    
    # Create a dictionary of media owners and their comment counts
    wordcloud_data = dict(zip(owner_counts["Media Owner"], owner_counts["Comment Count"]))
    
    # Generate the wordcloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(wordcloud_data)
    
    # Plot the wordcloud
    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.title("Accounts You Commented On Most")
    plt.tight_layout()

    # Save the figure
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    plt.savefig(output_path)
    plt.close()


def load_data(data_path):
    """
    Load the comment data from the JSON file.
    
    Args:
        data_path (str): Path to the post_comments JSON file
        
    Returns:
        DataFrame: DataFrame containing media owners and comment counts
    """
    try:
        # Load JSON file
        with open(data_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Extract media owners from the data
        media_owners = []
        for comment in data:
            try:
                media_owner = comment["string_map_data"].get("Media Owner", {}).get("value", "Unknown")
                media_owners.append(media_owner)
            except (KeyError, TypeError):
                media_owners.append("Unknown")

        # Create a DataFrame and count occurrences
        df = pd.DataFrame({"Media Owner": media_owners})
        owner_counts = df["Media Owner"].value_counts().reset_index()
        owner_counts.columns = ["Media Owner", "Comment Count"]
        owner_counts = owner_counts[owner_counts["Media Owner"] != "Unknown"]
        
        return owner_counts
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame(columns=["Media Owner", "Comment Count"])


def process_comments(input_folder, output_path=None):
    """
    Process comments data and generate visualization.
    
    Args:
        input_folder (str): Path to the folder containing the data files
        output_path (str, optional): Path to save the visualization
    """
    # Set default output path if not provided
    if output_path is None:
        output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                 "images", "post_comments.png")
    
    # Find the post_comments file in the input folder
    comments_path = os.path.join(input_folder, "post_comments_1.json")
    
    if not os.path.exists(comments_path):
        print(f"Error: Could not find post_comments_1.json in {input_folder}")
        return False
    
    # Load and process the data
    owner_counts = load_data(comments_path)
    
    if not owner_counts.empty:
        most_commented_barchart(owner_counts, output_path)
        return True
    else:
        return False


def main():
    # Check if a folder path was provided as a command-line argument
    if len(sys.argv) > 1:
        input_folder = sys.argv[1]
        output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                 "images", "post_comments.png")
        
        success = process_comments(input_folder, output_path)
        if success:
            print(f"Visualization created at {output_path}")
        else:
            print("Failed to create visualization")
    else:
        print("Please provide a folder path as a command-line argument")


if __name__ == "__main__":
    main()