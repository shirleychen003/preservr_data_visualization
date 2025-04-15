# Preservr Archive Visual Analysis Tool

The Preservr Archive Visual Analysis Tool (AVAT) is a tool for understanding your social media presence in broad strokes, so that you can make more informed decisions when archiving your Instagram data. It provides visual analysis of Instagram archive data, helping you understand your online interactions and engagement patterns.

## Prerequisites

### Installing Python

#### Windows
1. Visit the [Python downloads page](https://www.python.org/downloads/)
2. Download the latest Python 3 installer (recommended: Python 3.10 or newer)
3. Run the installer
4. **Important**: Check "Add Python to PATH" during installation
5. Click "Install Now" for the standard installation

#### macOS
1. Visit the [Python downloads page](https://www.python.org/downloads/)
2. Download the latest Python 3 installer for macOS
3. Run the installer package and follow the instructions
4. Alternatively, if you have Homebrew installed, open Terminal and run:
   ```
   brew install python
   ```

### Verifying Installation
To verify Python was installed correctly, open a terminal (Command Prompt on Windows or Terminal on macOS) and run:
```
python --version
```
You should see the Python version number displayed.

## Installation

### Windows
1. Download or clone this repository to your local machine
2. Open Command Prompt
3. Navigate to the project directory:
   ```
   cd path\to\preservr_data_visualization
   ```
4. Install the required dependencies:
   ```
   pip install pandas matplotlib wordcloud pillow
   ```

### macOS
1. Download or clone this repository to your local machine
2. Open Terminal
3. Navigate to the project directory:
   ```
   cd path/to/preservr_data_visualization
   ```
4. Install the required dependencies:
   ```
   pip3 install pandas matplotlib wordcloud pillow
   ```

## Dependencies
The following Python packages are required:

- pandas - Data analysis and manipulation
- matplotlib - Visualization library
- wordcloud - Word cloud generator
- pillow - Python Imaging Library (used for image processing)
- json (Built-in, no installation needed)
- collections (Built-in, no installation needed)

## Running the Application

### Windows
1. Open Command Prompt
2. Navigate to the project directory
3. Run the main script:
   ```
   python preservr.py
   ```

### macOS
1. Open Terminal
2. Navigate to the project directory
3. Run the main script:
   ```
   python3 preservr.py
   ```

## Usage
1. Launch the application
2. Click "Select Folder" to choose your Instagram archive folder
3. Choose an analysis option from the available buttons
4. View the generated visualizations in the application window

## Troubleshooting
If you encounter issues installing dependencies, try upgrading pip:

- Windows: `python -m pip install --upgrade pip`
- macOS: `pip3 install --upgrade pip`

For other issues, please open an issue on the GitHub repository.
