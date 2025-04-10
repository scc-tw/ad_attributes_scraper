"""
Git repository management for the Microsoft Win32 docs
"""

import os
import subprocess
import sys
from pathlib import Path
from typing import Optional


class RepoManager:
    """Manages the Git repository for Win32 documentation."""

    def __init__(
        self,
        repo_url: str = "https://github.com/MicrosoftDocs/win32.git",
        clone_dir: str = "win32_repo",
    ):
        """Initialize with repository URL and clone directory."""
        self.repo_url = repo_url
        self.clone_dir = clone_dir
        self.schema_dir = os.path.join(self.clone_dir, "desktop-src", "ADSchema")

    def ensure_repo_exists(self) -> str:
        """
        Ensures the repository exists locally, cloning if necessary.
        Returns the path to the schema directory.
        """
        if not os.path.exists(self.clone_dir):
            self._clone_repo()
        return self.get_schema_dir()

    def _clone_repo(self) -> None:
        """Clones the repository to the local file system."""
        print(
            f"Cloning repository from {self.repo_url} into {self.clone_dir}",
            file=sys.stderr,
        )
        try:
            subprocess.check_call(["git", "clone", self.repo_url, self.clone_dir])
        except subprocess.CalledProcessError as e:
            print(f"Error cloning repository: {e}", file=sys.stderr)
            sys.exit(1)
        print(f"Repository successfully cloned.", file=sys.stderr)

    def get_schema_dir(self) -> str:
        """
        Returns the path to the schema directory.
        Raises FileNotFoundError if the directory doesn't exist.
        """
        if not os.path.exists(self.schema_dir):
            print(
                f"Error: Schema directory not found at {self.schema_dir}",
                file=sys.stderr,
            )
            sys.exit(1)
        return self.schema_dir
