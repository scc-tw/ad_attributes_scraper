"""
Data models for AD attributes
"""

from dataclasses import dataclass
from typing import Dict, Optional, List, Any


@dataclass
class ADAttribute:
    """Represents an Active Directory attribute with its metadata."""

    display_name: str
    url: str
    raw_name: str
    schema_data: Optional[Dict[str, Any]] = None
