#!/usr/bin/env python3
# file: main.py

import sys
from src.scraper.web_scraper import AttributesScraper
from src.repo.git_manager import RepoManager
from src.parser.schema_parser import SchemaParser
from src.generator.cpp_generator import CppGenerator


def main():
    """
    Main function that orchestrates the AD attribute scraping process.
    Steps:
    1. Scrape attributes from Microsoft Learn
    2. Clone/update the repository
    3. Parse schema files for each attribute
    4. Generate C++ header file
    """
    # Step 1: Scrape the attribute list from Microsoft Learn
    target_url = (
        "https://learn.microsoft.com/en-us/windows/win32/adschema/attributes-all"
    )
    print("Step 1: Scraping attribute list from Microsoft Learn...")
    scraper = AttributesScraper(target_url)
    attributes = scraper.fetch_attributes()
    if not attributes:
        print("Failed to fetch attribute list. Exiting.", file=sys.stderr)
        sys.exit(1)
    print(f"Found {len(attributes)} attributes.")

    # Step 2: Setup the repository and get the schema directory
    print("\nStep 2: Setting up the repository...")
    repo_manager = RepoManager()
    schema_dir = repo_manager.ensure_repo_exists()
    print(f"Schema directory: {schema_dir}")

    # Step 3: Parse schema files for each attribute
    print("\nStep 3: Parsing schema files...")
    schema_parser = SchemaParser()
    processed_attributes = schema_parser.parse_schema_files(attributes, schema_dir)
    print(
        f"Successfully processed {len(processed_attributes)} attributes with schema data."
    )

    # Step 4: Generate the C++ header file
    print("\nStep 4: Generating C++ header file...")
    header_file = "AD_SCHEMA_ATTRIBUTES.hpp"
    cpp_generator = CppGenerator()
    cpp_generator.generate_header(processed_attributes, header_file)
    print(f"Successfully generated header file: {header_file}")
    print("\nDone!")


if __name__ == "__main__":
    main()
