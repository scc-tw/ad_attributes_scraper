#! /usr/bin/env python3
# file: modules/attributes_scraper.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys

class AttributesScraper:
    def __init__(self, url: str):
        self.url = url

    def get_formatted_attribute_list(self):
        """
        Fetches a webpage, extracts AD attribute names and links,
        formats the names (hyphen to underscore), handles relative hrefs,
        and returns a sorted list of (modified_attribute_name, absolute_url) tuples.
        """
        try:
            headers = {
                "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                               "AppleWebKit/537.36 (KHTML, like Gecko) "
                               "Chrome/91.0.4472.124 Safari/537.36")
            }
            print(f"Attempting to fetch URL: {self.url}", file=sys.stderr)
            response = requests.get(self.url, headers=headers, timeout=15)
            response.raise_for_status()
            print("Successfully fetched page content.", file=sys.stderr)

            soup = BeautifulSoup(response.text, "html.parser")
            print("Successfully parsed HTML.", file=sys.stderr)

            main_content = soup.find("main", id="main")
            if not main_content:
                print("Error: Could not find the main content area (<main id='main'>).", file=sys.stderr)
                return None
            print("Found main content area.", file=sys.stderr)

            potential_links = main_content.find_all("a", href=True)
            print(f"Found {len(potential_links)} potential links in main content.", file=sys.stderr)

            attribute_details = []
            processed_count = 0

            for link in potential_links:
                href = link.get("href")
                link_text = link.get_text(strip=True)
                # Only select links with hrefs starting with "a-" and which do not include "/" or ":"
                if (href and href.startswith("a-") and "/" not in href and ":" not in href and link_text):
                    # Replace hyphen with underscore in the display name
                    modified_name = link_text.replace("-", "_")
                    # Construct the absolute URL from the relative link
                    absolute_url = urljoin(self.url, href)
                    attribute_details.append((modified_name, absolute_url))
                    processed_count += 1

            print(f"Processed {processed_count} attribute-specific links.", file=sys.stderr)

            unique_details = list(set(attribute_details))
            unique_details.sort(key=lambda item: item[0])
            print(f"Returning {len(unique_details)} unique, sorted attributes.", file=sys.stderr)

            return unique_details

        except requests.exceptions.Timeout:
            print(f"Error: The request to {self.url} timed out.", file=sys.stderr)
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error during requests to {self.url}: {e}", file=sys.stderr)
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)
            return None

# For module testing:
if __name__ == "__main__":
    target_url = "https://learn.microsoft.com/en-us/windows/win32/adschema/attributes-all"
    scraper = AttributesScraper(target_url)
    details_list = scraper.get_formatted_attribute_list()
    if details_list:
        for name, url in details_list:
            print(f"{name}: {url}")

