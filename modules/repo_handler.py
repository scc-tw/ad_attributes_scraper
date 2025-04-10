#! /usr/bin/env python3
# file: modules/repo_handler.py

import os
import subprocess
import sys


class RepoManager:
    def __init__(
        self,
        repo_url: str = "https://github.com/MicrosoftDocs/win32.git",
        clone_dir: str = "win32_repo",
    ):
        self.repo_url = repo_url
        self.clone_dir = clone_dir

    def clone_repo(self):
        """
        Clones the repository if the clone directory doesn't exist.
        """
        if not os.path.exists(self.clone_dir):
            print(f"Cloning repository from {self.repo_url} into {self.clone_dir}")
            try:
                subprocess.check_call(["git", "clone", self.repo_url, self.clone_dir])
            except subprocess.CalledProcessError as e:
                print(f"Error cloning repository: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            print(f"Repository already cloned into {self.clone_dir}")

    def get_schema_dir(self) -> str:
        """
        Returns the path to the ADSchema folder.
        The schema files are expected to be in:
            <clone_dir>/win32/desktop-src/ADSchema
        """
        schema_dir = os.path.join(self.clone_dir, "desktop-src", "ADSchema")
        if not os.path.exists(schema_dir):
            print(f"Error: Schema directory not found at {schema_dir}", file=sys.stderr)
            sys.exit(1)
        return schema_dir


# For module testing:
if __name__ == "__main__":
    repo_manager = RepoManager()
    repo_manager.clone_repo()
    print("Schema directory:", repo_manager.get_schema_dir())
