"""
Web scraper for Microsoft AD schema attributes
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import List
import sys

from src.models import ADAttribute


class AttributesScraper:
    """Scrapes AD attributes from Microsoft Learn website."""

    def __init__(self, url: str):
        """Initialize with the target URL."""
        self.url = url
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            )
        }

    def fetch_attributes(self) -> List[ADAttribute]:
        """
        Fetches the webpage, extracts AD attribute names and links,
        and returns a list of ADAttribute objects.
        """
        try:
            print(f"Attempting to fetch URL: {self.url}", file=sys.stderr)
            response = requests.get(self.url, headers=self.headers, timeout=15)
            response.raise_for_status()
            print("Successfully fetched page content.", file=sys.stderr)

            soup = BeautifulSoup(response.text, "html.parser")
            print("Successfully parsed HTML.", file=sys.stderr)

            main_content = soup.find("main", id="main")
            if not main_content:
                print("Error: Could not find the main content area.", file=sys.stderr)
                return []
            print("Found main content area.", file=sys.stderr)

            potential_links = main_content.find_all("a", href=True)
            print(
                f"Found {len(potential_links)} potential links in main content.",
                file=sys.stderr,
            )

            attributes = []
            processed_count = 0

            for link in potential_links:
                href = link.get("href")
                link_text = link.get_text(strip=True)

                # Only select links with hrefs starting with "a-" and which do not include "/" or ":"
                if (
                    href
                    and href.startswith("a-")
                    and "/" not in href
                    and ":" not in href
                    and link_text
                ):
                    display_name = link_text.replace("-", "_")
                    absolute_url = urljoin(self.url, href)
                    raw_name = href[2:]  # Remove "a-" prefix

                    attributes.append(
                        ADAttribute(
                            display_name=display_name,
                            url=absolute_url,
                            raw_name=raw_name,
                        )
                    )
                    processed_count += 1

            print(
                f"Processed {processed_count} attribute-specific links.",
                file=sys.stderr,
            )

            # Sort attributes by display name
            attributes.sort(key=lambda attr: attr.display_name)
            print(f"Returning {len(attributes)} sorted attributes.", file=sys.stderr)

            return attributes

        except requests.exceptions.RequestException as e:
            print(f"Error during request to {self.url}: {e}", file=sys.stderr)
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)
            return []
