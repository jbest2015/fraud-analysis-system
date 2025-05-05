# Fraud Data Analysis Database

This project organizes fraud incident data into a SQLite database for analysis and reporting with a PyQt6-based GUI interface.

## Features

- Data import from JSON to SQLite database
- Modern PyQt6-based GUI interface
- Filtering and search capabilities
- Detailed incident view with multiple tabs
- Transaction tracking
- Investigation notes viewer

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Import data and run the GUI:
```bash
# First import the data
python src/main.py

# Then run the GUI
python src/gui_app.py
```