"""
C++ header generator for AD schema attributes
"""

import re
import sys
from typing import List, TextIO

from src.models import ADAttribute


class CppGenerator:
    """Generates C++ header files from AD attribute data."""

    def generate_header(self, attributes: List[ADAttribute], output_file: str) -> None:
        """
        Generates a C++ header file from the processed attributes.
        """
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                self._write_header_guard(f)
                self._write_includes(f)
                self._write_struct_definition(f)
                self._write_enum_class(f, attributes)
                self._write_schema_entities(f, attributes)
                self._write_mapping(f, attributes)
                self._write_footer(f)

            print(f"Header file generated at {output_file}", file=sys.stderr)
        except IOError as e:
            print(f"Error writing header file: {e}", file=sys.stderr)
            sys.exit(1)

    def _write_header_guard(self, f: TextIO) -> None:
        """Writes the header guard to the file."""
        f.write("#pragma once\n")
        f.write("#ifndef AD_SCHEMA_ATTRIBUTES_HPP\n")
        f.write("#define AD_SCHEMA_ATTRIBUTES_HPP\n\n")

    def _write_includes(self, f: TextIO) -> None:
        """Writes the necessary include statements to the file."""
        f.write("#include <array>\n")
        f.write("#include <string_view>\n")
        f.write("#include <unordered_map>\n\n")

    def _write_struct_definition(self, f: TextIO) -> None:
        """Writes the struct definition to the file."""
        f.write("struct ADSchemaEntity {\n")
        f.write("    std::string_view CN;\n")
        f.write("    std::string_view ldap_display_name;\n")
        f.write("    std::string_view attribute_id;\n")
        f.write("    std::string_view system_Id_guid;\n")
        f.write("    int size;\n")
        f.write("};\n\n")

    def _write_enum_class(self, f: TextIO, attributes: List[ADAttribute]) -> None:
        """Writes the enum class definition to the file."""
        f.write("enum class OidType {\n")
        for attr in attributes:
            f.write(f"    {attr.display_name},\n")
        f.write("};\n\n")

    def _write_schema_entities(self, f: TextIO, attributes: List[ADAttribute]) -> None:
        """Writes the schema entities array to the file."""
        f.write("static inline constexpr ADSchemaEntity schemaEntities[] = {\n")
        for attr in attributes:
            data = attr.schema_data

            # Extract values with safe defaults
            cn = self._escape_string(data.get("CN", ""))
            ldap_display_name = self._escape_string(data.get("Ldap-Display-Name", ""))
            attribute_id = self._escape_string(data.get("Attribute-Id", ""))
            system_id_guid = self._escape_string(data.get("System-Id-Guid", ""))

            # Handle size specially
            size = data.get("Size", 0)
            if not isinstance(size, int):
                match = re.search(r"\d+", str(size))
                if match:
                    size = int(match.group())
                else:
                    size = 0

            # Write the entity
            f.write(
                f"""    {{
        .CN = "{cn}",
        .ldap_display_name = "{ldap_display_name}",
        .attribute_id = "{attribute_id}",
        .system_Id_guid = "{system_id_guid}",
        .size = {size}
    }},\n"""
            )
        f.write("};\n\n")

    def _write_mapping(self, f: TextIO, attributes: List[ADAttribute]) -> None:
        """Writes the mapping from enum values to entities."""
        f.write(
            "static inline const std::unordered_map<OidType, const ADSchemaEntity&> oidToEntityMapping = {\n"
        )
        for i, attr in enumerate(attributes):
            f.write(f"    {{ OidType::{attr.display_name}, schemaEntities[{i}] }},\n")
        f.write("};\n\n")

    def _write_footer(self, f: TextIO) -> None:
        """Writes the closing header guard to the file."""
        f.write("#endif // AD_SCHEMA_ATTRIBUTES_HPP\n")

    def _escape_string(self, s: str) -> str:
        """Escapes quotes in strings for safe use in C++ string literals."""
        return s.replace('"', '\\"')
