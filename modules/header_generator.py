#! /usr/bin/env python3
# file: modules/header_generator.py

import sys
import json
import re


def escape(s: str) -> str:
    """Escape embedded quotes for safe use in C++ string literals."""
    return s.replace('"', '\\"')


def generate_header(input_json: str, output_header: str):
    """
    Reads the schema data from input_json and generates a C++ header file at output_header.
    """
    try:
        with open(input_json, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error reading JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error opening file: {e}", file=sys.stderr)
        sys.exit(1)

    with open(output_header, "w", encoding="utf-8") as f:
        # Write header guard and includes.
        f.write("#pragma once\n")
        f.write("#ifndef AD_SCHEMA_ATTRIBUTES_HPP\n")
        f.write("#define AD_SCHEMA_ATTRIBUTES_HPP\n\n")
        f.write("#include <array>\n")
        f.write("#include <string_view>\n")
        f.write("#include <unordered_map>\n\n")
        f.write("struct ADSchemaEntity {\n")
        f.write("    std::string_view CN;\n")
        f.write("    std::string_view ldap_display_name;\n")
        f.write("    std::string_view attribute_id;\n")
        f.write("    std::string_view system_Id_guid;\n")
        f.write("    int size;\n")
        f.write("};\n\n")

        # Generate enum class OidType
        f.write("enum class OidType {\n")
        seen = set()
        for entry in data:
            enum_name = entry.get("markdown_link", "")
            if not enum_name or enum_name in seen:
                continue
            seen.add(enum_name)
            f.write(f"    {enum_name}, \n")
        f.write("};\n\n")

        # Output schemaEntities as a constant C array
        f.write("constexpr ADSchemaEntity schemaEntities[] = {\n")
        for entry in data:
            cn = escape(entry.get("CN", ""))
            ldap_disp = escape(entry.get("Ldap-Display-Name", ""))
            attribute_id = escape(entry.get("Attribute-Id", ""))
            system_id_guid = escape(entry.get("System-Id-Guid", ""))
            size = entry.get("Size", 0)
            if not isinstance(size, int):
                match = re.search(r"\d+", str(size))
                if match:
                    size = int(match.group())
                else:
                    size = 0
            f.write(
                f'    {{ .CN = "{cn}", .ldap_display_name = "{ldap_disp}", .attribute_id = "{attribute_id}", .system_Id_guid = "{system_id_guid}", .size = {size} }},\n'
            )
        f.write("};\n\n")

        # Build the mapping from enum values to entities.
        mapping_entries = []
        for i, entry in enumerate(data):
            enum_name = entry.get("markdown_link", "")
            if not enum_name:
                continue
            mapping_entries.append((enum_name, i))

        f.write(
            "const std::unordered_map<OidType, const ADSchemaEntity&> oidToEntityMapping = {\n"
        )
        for enum_name, i in mapping_entries:
            f.write(f"    {{ OidType::{enum_name}, schemaEntities[{i}] }},\n")
        f.write("};\n\n")

        f.write("#endif // AD_SCHEMA_ATTRIBUTES_HPP\n")

    print(f"Header file generated at {output_header}")


# For module testing:
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} input.json output_header.h", file=sys.stderr)
        sys.exit(1)
    input_json = sys.argv[1]
    output_header = sys.argv[2]
    generate_header(input_json, output_header)
