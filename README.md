# AD Attributes Scraper

A tool to scrape Active Directory schema attributes from Microsoft documentation and generate a C++ header file.

## Overview

This project scrapes AD schema attributes from Microsoft Learn, processes the schema information from the Microsoft documentation repository, and generates a C++ header file for easy inclusion in C++ projects.

## Features

- Scrapes AD attribute details from Microsoft Learn
- Clones the Microsoft Win32 documentation repository
- Parses schema information from Markdown files
- Generates a C++ header file with schema information

## Requirements

- Python 3.13 or higher
- Git (for cloning the documentation repository)
- Poetry (optional, for dependency management)

## Installation

1. Clone this repository:
```bash
git clone https://github.com/your-username/ad-attributes-scraper.git
cd ad-attributes-scraper
```

2. Install dependencies:
```bash
# Using pip
pip install -r requirements.txt

# Or using Poetry
poetry install
```

## Usage

Run the script:
```bash
# Using Python directly
python main.py

# Or using Poetry
poetry run scraper
```

The script will:
1. Scrape AD attributes from Microsoft Learn
2. Clone the Microsoft Win32 documentation repository
3. Process schema files
4. Generate a C++ header file (`AD_SCHEMA_ATTRIBUTES.hpp`)

## Project Structure

```
ad_attributes_scraper/
├── src/                      # Source code
│   ├── scraper/              # Web scraping utilities
│   ├── repo/                 # Git repository management
│   ├── parser/               # Schema parsing utilities
│   ├── generator/            # C++ header generation
│   └── models.py             # Data models
├── main.py                   # Main entry point
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## License

Cycraft 