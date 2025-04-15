PRESERVR
========

A toolkit for analyzing your social media presence online.
Provides visual analysis of Instagram archive data to help you
understand your interactions and engagement patterns.

PREREQUISITES
-------------

1. Installing Python

   Windows:
     1. Go to https://www.python.org/downloads/
     2. Download the latest Python 3 installer (3.10+ recommended)
     3. Run the installer
     4. IMPORTANT: Check “Add Python to PATH”
     5. Click “Install Now”

   macOS:
     1. Go to https://www.python.org/downloads/
     2. Download the latest macOS installer
     3. Run the installer and follow instructions
     OR, if you have Homebrew:
       • Open Terminal and run:
         brew install python

2. Verifying Installation

   Open a terminal (Command Prompt on Windows or Terminal on macOS) and run:
     python --version

   You should see your Python version displayed.

INSTALLATION
------------

1. Windows

   a. Download or clone this repository to your machine.
   b. Open Command Prompt.
   c. Navigate to the project folder:
        cd path\to\preservr_data_visualization
   d. Install dependencies:
        pip install pandas matplotlib wordcloud pillow

2. macOS

   a. Download or clone this repository to your machine.
   b. Open Terminal.
   c. Navigate to the project folder:
        cd path/to/preservr_data_visualization
   d. Install dependencies:
        pip3 install pandas matplotlib wordcloud pillow

DEPENDENCIES
------------

- pandas     — Data analysis and manipulation  
- matplotlib — Visualization library  
- wordcloud  — Word‑cloud generator  
- pillow     — Python Imaging Library  
- json       — Built‑in (no install needed)  
- collections — Built‑in (no install needed)  

RUNNING THE APPLICATION
-----------------------

1. Windows

   a. Open Command Prompt.
   b. Navigate to the project folder.
   c. Run:
        `python preservr.py` or click preservr.py in the directory

2. macOS

   a. Open Terminal.
   b. Navigate to the project folder.
   c. Run:
        `python3 preservr.py` or click preservr.py in the directory

USAGE
-----

1. Launch the application.
2. Click “Select Folder” and choose your Instagram archive folder.
3. Pick an analysis option.
4. View the generated visualizations.

TROUBLESHOOTING
---------------

- If dependency install fails, upgrade pip:
    • Windows: python -m pip install --upgrade pip  
    • macOS:   pip3 install --upgrade pip

- For any other issues, please open an issue on the GitHub repository.
