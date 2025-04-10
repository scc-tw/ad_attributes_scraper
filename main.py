#! /usr/bin/env python3
# file: main.py

import sys
from modules.attributes_scraper import AttributesScraper
from modules.schema_parser import (
    parse_attributes_from_markdown,
    process_schema_files,
    save_schema_data_to_json,
)
from modules.header_generator import generate_header
from modules.repo_handler import RepoManager


def generate_markdown(attributes: list, output_file: str = "attributes_list.md"):
    """
    Generates a Markdown file with a list of attributes.
    Each entry is written as a Markdown link.
    """
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(
                f"## Active Directory Schema Attributes ({len(attributes)} Found)\n\n"
            )
            f.write("-" * 40 + "\n")
            for name, link_url in attributes:
                f.write(f"- [{name}]({link_url})\n")
            f.write("-" * 40 + "\n")
        print(f"Markdown file generated at {output_file}")
    except IOError as e:
        print(f"Error writing to file {output_file}: {e}", file=sys.stderr)


def main():
    # Step 1: Scrape the attribute list from Microsoft Learn
    target_url = (
        "https://learn.microsoft.com/en-us/windows/win32/adschema/attributes-all"
    )
    scraper = AttributesScraper(target_url)
    details_list = scraper.get_formatted_attribute_list()
    if not details_list:
        print("Failed to fetch attribute list. Exiting.", file=sys.stderr)
        sys.exit(1)
    markdown_file = "attributes_list.md"
    generate_markdown(details_list, markdown_file)

    # Step 1.5: Automatically clone the repository and get the schema directory.
    repo_manager = RepoManager()
    repo_manager.clone_repo()
    schema_dir = repo_manager.get_schema_dir()

    # Step 2 & 3: Process the Markdown to produce schema JSON data
    attributes = parse_attributes_from_markdown(markdown_file)
    schema_data = process_schema_files(attributes, schema_dir)
    json_file = "ad_schema_attributes.json"
    save_schema_data_to_json(schema_data, json_file)

    # Step 4: Generate C++ header from the JSON data
    header_file = "AD_SCHEMA_ATTRIBUTES.hpp"
    generate_header(json_file, header_file)


if __name__ == "__main__":
    main()
