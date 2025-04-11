# AD Schema Attributes for C++

> Generate a C++ header file of Active Directory schema attributes for easy integration into your projects.

![License: Cycraft](https://img.shields.io/badge/license-Cycraft-blue)
![Monthly Releases](https://img.shields.io/badge/releases-monthly-green)

## 📋 Overview

This tool extracts Active Directory schema attributes from Microsoft's official documentation and creates a ready-to-use C++ header file. 

The generated `AD_SCHEMA_ATTRIBUTES.hpp` file provides:
- A complete `enum class OidType` with all AD attribute types
- Metadata for each attribute (LDAP names, GUIDs, etc.)
- Proper C++ structure for easy integration

## 🚀 Quick Start

### Option 1: Use Pre-built Header

**The fastest way to get started** is to download the latest header file from our [Releases](https://github.com/scc-tw/ad_attributes_scraper/releases) page.

### Option 2: Generate Your Own Header

1. Clone this repository:
   ```bash
   git clone https://github.com/scc-tw/ad_attributes_scraper.git
   cd ad_attributes_scraper
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Run the script:
   ```bash
   python main.py
   ```

4. Find your generated header in the root directory: `AD_SCHEMA_ATTRIBUTES.hpp`

## 🔧 Adding to Your C++ Project

### Requirements

- C++20 or later (due to Designated Initializers since C++20, std::string_iew since C++17, static inline to against ODR-used)
  - If you're only using features like `std::unordered_map` and `constexpr`, you can downgrade to C++11. However, C++20 is recommended for its enhanced capabilities.
- CMake 3.14 or later (for automatic updates)

### With CMake (Recommended)

CMake makes it easy to automatically download and include the header file. Add this to your `CMakeLists.txt`:

```cmake
# Quick setup - specific version
include(FetchContent)
FetchContent_Declare(
    ad_schema_header
    URL https://github.com/scc-tw/ad_attributes_scraper/releases/download/v2025.04.10/AD_SCHEMA_ATTRIBUTES.hpp
    DOWNLOAD_NO_EXTRACT TRUE
    DOWNLOAD_DIR "${CMAKE_CURRENT_BINARY_DIR}/include"
    DOWNLOAD_NAME "AD_SCHEMA_ATTRIBUTES.hpp"
)
FetchContent_MakeAvailable(ad_schema_header)
include_directories("${CMAKE_CURRENT_BINARY_DIR}/include")
```

### Without Build Systems

Simply download the `AD_SCHEMA_ATTRIBUTES.hpp` file and place it in your project's include directory.

## 🧩 Using the Header

Once included, you can use the schema attributes in your code:

```cpp
#include "AD_SCHEMA_ATTRIBUTES.hpp"

int main() {
    // Use OidType enum values
    OidType attribute = OidType::User_Principal_Name;
    
    // Access schema metadata for an attribute
    std::unordered_map<OidType, ADSchemaEntity, OidTypeHash, OidTypeEqual> schemaMap;
    schemaMap[OidType::Common_Name] = {"CN", "cn", "2.5.4.3", "bf967a0e-0de6-11d0-a285-00aa003049e2", 64};
    
    // Use the metadata
    std::cout << "LDAP Name: " << schemaMap[OidType::Common_Name].ldap_display_name << std::endl;
    return 0;
}
```

## 🔄 Advanced: Auto-Update to Latest Version

For projects that want to **always use the latest schema**, this CMake snippet automatically fetches the newest release:

```cmake
cmake_minimum_required(VERSION 3.14)
project(YourProject)

include(FetchContent)

# Function to download the latest release version
function(get_latest_release_version owner repo output_variable)
    set(api_url "https://api.github.com/repos/${owner}/${repo}/releases/latest")
    set(json_file "${CMAKE_CURRENT_BINARY_DIR}/latest_release.json")
    
    # Download with timeout and progress indicator
    file(DOWNLOAD
        "${api_url}"
        "${json_file}"
        TIMEOUT 10
        STATUS download_status
        SHOW_PROGRESS
        HTTPHEADER "Accept: application/vnd.github.v3+json"
        HTTPHEADER "User-Agent: CMake/${CMAKE_VERSION}"
    )
    
    # Check if download was successful
    list(GET download_status 0 status_code)
    if(NOT status_code EQUAL 0)
        message(STATUS "Using fallback version")
        set(${output_variable} "v2025.04.10" PARENT_SCOPE) # Fallback to a known version
        return()
    endif()
    
    # Read and parse the JSON
    file(READ "${json_file}" json_content)
    string(JSON tag_name ERROR_VARIABLE json_error GET "${json_content}" "tag_name")
    
    if(NOT json_error STREQUAL "NOTFOUND")
        message(STATUS "Using fallback version")
        set(${output_variable} "v2025.04.10" PARENT_SCOPE) # Fallback to a known version
    else()
        set(${output_variable} ${tag_name} PARENT_SCOPE)
    endif()
endfunction()

# Get the latest release version
get_latest_release_version("scc-tw" "ad_attributes_scraper" LATEST_VERSION)
message(STATUS "Using AD_SCHEMA release: ${LATEST_VERSION}")

# Download the header
FetchContent_Declare(
    ad_schema_header
    URL "https://github.com/scc-tw/ad_attributes_scraper/releases/download/${LATEST_VERSION}/AD_SCHEMA_ATTRIBUTES.hpp"
    DOWNLOAD_NO_EXTRACT TRUE
    DOWNLOAD_DIR "${CMAKE_CURRENT_BINARY_DIR}/include"
    DOWNLOAD_NAME "AD_SCHEMA_ATTRIBUTES.hpp"
    TIMEOUT 20
    TLS_VERIFY ON
)
FetchContent_MakeAvailable(ad_schema_header)
include_directories("${CMAKE_CURRENT_BINARY_DIR}/include")

# Add a custom target to refresh the header file
add_custom_target(update_ad_schema
    COMMAND ${CMAKE_COMMAND} -E remove -f "${CMAKE_CURRENT_BINARY_DIR}/include/AD_SCHEMA_ATTRIBUTES.hpp"
    COMMAND ${CMAKE_COMMAND} -E remove -f "${CMAKE_CURRENT_BINARY_DIR}/latest_release.json"
    COMMAND ${CMAKE_COMMAND} --build ${CMAKE_BINARY_DIR} --target ad_schema_header-populate
    COMMENT "Updating AD_SCHEMA_ATTRIBUTES.hpp to the latest version"
)

# Your executable
add_executable(your_app main.cpp)
```

To manually update to the latest schema at any time:
```bash
cmake --build build --target update_ad_schema
```

## 📆 Automated Monthly Releases

This repository automatically creates a new release on the first day of every month, ensuring you always have access to the most current AD schema attributes.

Each release:
- Is tagged with format `vYYYY.MM.DD` (year.month.day)
- Contains the freshly generated `AD_SCHEMA_ATTRIBUTES.hpp` file

### Triggering a Manual Release

1. Go to the Actions tab in the GitHub repository
2. Select the "Monthly AD Schema Release" workflow
3. Click "Run workflow"

## 🛠️ Project Structure

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
├── LICENSE.txt               # License
└── README.md                 # This file
```

## 📄 License

This project is licensed under the [Cycraft License](LICENSE.txt).

Cycraft 
