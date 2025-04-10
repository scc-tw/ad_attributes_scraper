"""
Schema parser for AD attribute markdown files
"""

import re
import os
from typing import Dict, List, Optional, Any

from src.models import ADAttribute


class SchemaParser:
    """Parses AD schema markdown files for attribute information."""

    def __init__(self):
        """Initialize the parser with regex patterns."""
        self.table_pattern = re.compile(
            r"\|\s*Entry\s*\|\s*Value\s*\|\n\|[-\s]*\|[-\s]*\|\n((?:\|[^|]*\|[^|]*\|\n)*)"
        )

    def parse_schema_files(
        self, attributes: List[ADAttribute], schema_dir: str
    ) -> List[ADAttribute]:
        """
        Processes each attribute in the list, finding and parsing its schema file.
        Returns a filtered list of attributes that have schema data.
        """
        processed_attributes = []

        for attr in attributes:
            filename = f"a-{attr.raw_name}.md"
            file_path = os.path.join(schema_dir, filename)

            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()

                schema_data = self.parse_table_to_dict(content)
                if schema_data:
                    attr.schema_data = schema_data
                    processed_attributes.append(attr)

        return processed_attributes

    def parse_table_to_dict(self, content: str) -> Optional[Dict[str, Any]]:
        """
        Parses a Markdown table with Entry|Value format into a dictionary.
        Returns None if the table cannot be found or parsed.
        """
        table_match = self.table_pattern.search(content)
        if not table_match:
            return None

        table_content = table_match.group(1)
        attr_dict = {}

        for line in table_content.strip().split("\n"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 3:
                key = parts[1]
                value = parts[2]

                # Process the value
                value = self._process_value(key, value)
                attr_dict[key] = value

        # Add markdown_link field for compatibility with existing code
        return attr_dict

    def _process_value(self, key: str, value: str) -> Any:
        """Processes a value based on its key and content."""
        # Remove Markdown links
        value = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", value)

        # Handle special cases
        if value in ("\\-", "-"):
            return ""
        elif key == "Size":
            if match := re.match(r"^\d+\s*bytes?$", value):
                return int(value.replace("bytes", "").strip())
        elif value.isdigit():
            return int(value)

        return value
