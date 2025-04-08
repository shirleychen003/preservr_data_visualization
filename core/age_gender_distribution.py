"""
Preservr Data Visualizations - Age Distribution by Gender
Author: Shirley Chen
Description: This module provides visualization tools for analyzing and displaying
             follower age distribution segmented by gender for the Preservr project.
             It extracts audience data from Instagram insights and generates a grouped
             bar chart to show how follower age groups are distributed across men and women.
Input: audience_insights.json file stored in the provided folder path.
Output: Visualization saved as age_distribution_by_gender.png in the same folder.
Date: 2025-04
"""

import os
import sys
import json
import matplotlib.pyplot as plt
import numpy as np

# For testing:
# Load JSON data
# with open('../test_data/audience_insights.json', 'r') as f:
#     data = json.load(f)

def find_file_in_subdirectories(folder_path, filename):
    """
    Recursively search for the specified file in subdirectories.
    """
    for root, dirs, files in os.walk(folder_path):
        if filename in files:
            return os.path.join(root, filename)
    return None

def parse_percentage_string(raw_str):
    """
    Convert a string of age:percentage pairs into a dictionary.
    Example: "18-24: 60.5%, 25-34: 20%" -> {'18-24': 60.5, '25-34': 20.0}
    """
    return {
        age.strip(): float(percent.strip().replace('%', ''))
        for age, percent in [segment.split(':') for segment in raw_str.split(',')]
    }

def generate_age_distribution_chart(folder_path):
    """
    Generate a grouped bar chart of follower age distribution by gender.
    """
    # Locate the JSON file
    input_path = find_file_in_subdirectories(folder_path, "audience_insights.json")
    if input_path is None:
        print(f"Error: audience_insights.json not found in {folder_path} or its subdirectories")
        return

    # Define output file path
    output_path = os.path.join(folder_path, "age_distribution_by_gender.png")

    # Load JSON data
    with open(input_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    string_data = data["organic_insights_audience"][0]["string_map_data"]

    # Extract total followers and gender distribution
    total_followers = int(string_data["Followers"]["value"].replace(',', ''))
    men_ratio = 0.43  # 43%
    women_ratio = 0.569  # 56.9%

    # Extract age distributions for each gender
    men_data = parse_percentage_string(string_data["Follower Percentage by Age for Men"]["value"])
    women_data = parse_percentage_string(string_data["Follower Percentage by Age for Women"]["value"])

    # Ensure consistent age group ordering
    age_groups = list(men_data.keys())

    # Convert percentages to counts
    men_counts = [round((pct / 100) * total_followers * men_ratio) for pct in men_data.values()]
    women_counts = [round((pct / 100) * total_followers * women_ratio) for pct in women_data.values()]

    # Plot grouped bar chart
    x = np.arange(len(age_groups))
    width = 0.35

    men_color = "#4A90E2"
    women_color = "#F15A5A"

    plt.figure(figsize=(10, 6))
    plt.bar(x - width/2, men_counts, width, label="Men", color=men_color)
    plt.bar(x + width/2, women_counts, width, label="Women", color=women_color)

    plt.xticks(x, age_groups)
    plt.xlabel("Age Group")
    plt.ylabel("Number of Followers")
    plt.title("Preservr Audience: Age Distribution by Gender")
    plt.legend()
    plt.tight_layout()

    # Save the figure
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Visualization saved to: {output_path}")

# Entry point for CLI usage
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python age_distribution_by_gender.py <folder_path>")
        sys.exit(1)

    folder = sys.argv[1]
    generate_age_distribution_chart(folder)
