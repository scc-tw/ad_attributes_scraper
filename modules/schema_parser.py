#! /usr/bin/env python3
# file: modules/schema_parser.py

import re
import os
import json


def parse_table_to_dict(content: str):
    """
    Parses a Markdown table (matching the 'Entry | Value' format)
    into a Python dictionary.
    """
    table_pattern = (
        r"\|\s*Entry\s*\|\s*Value\s*\|\n\|[-\s]*\|[-\s]*\|\n((?:\|[^|]*\|[^|]*\|\n)*)"
    )
    table_match = re.search(table_pattern, content)
    if not table_match:
        return None

    table_content = table_match.group(1)

    attr_dict = {}
    for line in table_content.strip().split("\n"):
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 3:
            key = parts[1]
            value = parts[2]
            # Remove Markdown links ([...](...))
            value = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", value)
            if value in ("\\-", "-"):
                value = ""
            elif key == "Size":
                if re.match(r"^\d+\s*bytes?$", value):
                    value = int(value.replace("bytes", "").strip())
            elif value.isdigit():
                value = int(value)
            attr_dict[key] = value
    return attr_dict


def parse_attributes_from_markdown(markdown_file: str):
    """
    Reads a Markdown file (like the generated attributes_list.md)
    and returns a mapping from display name to the attribute name extracted from the URL.
    """
    attributes = {}
    with open(markdown_file, "r", encoding="utf-8") as f:
        content = f.read()

    pattern = r"\[(.*?)\]\((.*?)a-(.*?)\)"
    matches = re.findall(pattern, content)
    for display_name, _, attr_name in matches:
        attributes[display_name] = attr_name
    return attributes


def process_schema_files(attributes: dict, schema_dir: str):
    """
    Iterates over each attribute in the mapping, reads the corresponding Markdown file
    (a-{attr_name}.md in the provided schema_dir), parses the table, and adds a 'markdown_link' field.

    Returns a list of attribute dictionaries.
    """
    result = []
    for display_name, attr_name in attributes.items():
        filename = f"a-{attr_name}.md"
        file_path = os.path.join(schema_dir, filename)
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                attr_dict = parse_table_to_dict(content)
                if attr_dict:
                    attr_dict["markdown_link"] = display_name
                    result.append(attr_dict)
    return result


def save_schema_data_to_json(
    schema_data: list, output_file: str = "ad_schema_attributes.json"
):
    """
    Saves the schema data (a list of dictionaries) into a JSON file.
    """
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(schema_data, f, indent=2)
    print(f"Successfully saved {len(schema_data)} attributes to {output_file}")


# For module testing:
if __name__ == "__main__":
    # Assumes attributes_list.md already exists in the current directory.
    attributes = parse_attributes_from_markdown("attributes_list.md")
    schema_data = process_schema_files(attributes)
    save_schema_data_to_json(schema_data)
