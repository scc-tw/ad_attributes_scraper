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
    # Step 1: Scrape the attribute and class lists from Microsoft Learn
    print("Step 1: Scraping attribute and class lists from Microsoft Learn...")

    list_pages = [
        "https://learn.microsoft.com/en-us/windows/win32/adschema/attributes-all",
        "https://learn.microsoft.com/en-us/windows/win32/adschema/classes-all",
    ]

    all_attributes = []
    for page_url in list_pages:
        print(f"Fetching list page: {page_url}")
        scraper = AttributesScraper(page_url)
        page_attrs = scraper.fetch_attributes()
        print(f"  -> Retrieved {len(page_attrs)} entries from this page.")
        all_attributes.extend(page_attrs)

    if not all_attributes:
        print("Failed to fetch any attribute/class list. Exiting.", file=sys.stderr)
        sys.exit(1)

    # Deduplicate by raw_name to avoid collisions between attribute and class pages
    unique_attr_map = {}
    for attr in all_attributes:
        if attr.raw_name not in unique_attr_map:
            unique_attr_map[attr.raw_name] = attr

    attributes = list(unique_attr_map.values())
    print(f"Found {len(attributes)} unique attributes/classes.")

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
