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
            # Documentation stores attribute pages under "a-" and class pages under
            # "c-".  We first look for the attribute style file and, if not
            # found, fall back to the class style file.

            possible_filenames = [f"a-{attr.raw_name}.md", f"c-{attr.raw_name}.md"]

            file_path: Optional[str] = None
            for fname in possible_filenames:
                candidate = os.path.join(schema_dir, fname)
                if os.path.exists(candidate):
                    file_path = candidate
                    break

            if file_path is None:
                continue  # No schema doc found – skip this attribute

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            schema_data = self.parse_table_to_dict(content)
            if schema_data:
                attr.schema_data = schema_data
                processed_attributes.append(attr)

        return processed_attributes

    def parse_table_to_dict(self, content: str) -> Optional[Dict[str, Any]]:
        """
        Parses ALL Markdown tables with an Entry|Value format into a single
        dictionary. Some schema pages contain additional metadata (for example
        *Governs-Id*) in subsequent tables rather than the first one.  By
        iterating over *all* matching tables we ensure those fields are
        captured.

        If a key already exists we **keep the first occurrence** (usually the
        first table found near the top of the document) to avoid unintentionally
        overriding core fields such as *CN* or *Ldap-Display-Name* that may be
        repeated for different Windows versions.

        Special case:  Some class definition pages expose the relevant OID in a
        *Governs-Id* field instead of *Attribute-Id*.  For convenience - and to
        maintain compatibility with the rest of the code-base - we copy the
        value from *Governs-Id* to *Attribute-Id* when the latter is missing.
        """

        matches = list(self.table_pattern.finditer(content))
        if not matches:
            return None

        attr_dict: Dict[str, Any] = {}

        for match in matches:
            table_content = match.group(1)

            for line in table_content.strip().split("\n"):
                parts = [p.strip() for p in line.split("|")]
                if len(parts) < 3:
                    continue

                key = parts[1]
                value = parts[2]

                # Process the value
                processed_value = self._process_value(key, value)

                # Preserve the first occurrence of each key
                if key not in attr_dict:
                    attr_dict[key] = processed_value

        # If Attribute-Id is missing but Governs-Id is present, use it.
        if "Attribute-Id" not in attr_dict and "Governs-Id" in attr_dict:
            attr_dict["Attribute-Id"] = attr_dict["Governs-Id"]

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
