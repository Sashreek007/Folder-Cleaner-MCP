"""
    Input validation utilites for MCP Folder Cleaner.
This module provides security-critical validation functions to prevent:
- Directory traversal attacks (accessing files outside allowed directories)
- Invalid filenames that could crash or exploit the system
- Pattern injection attacks
"""

from pathlib import Path
import re
from typing import Optional


def validate_path(path: Path, base_dir: Optional[Path] = None) -> bool:
    """
    Validate that a path is safe to operate on.

    This prevents directory traversal attacks and accidental system file operations.

    SECURITY CONCEPT: PATH TRAVERSAL (Also called Directory Traversal)
    Path traversal is when an attacker tries to access files outside the intended
    directory by using special path characters like ".." (parent directory).

    Example attack scenario:
    ------------------------
    User input: "../../../etc/passwd"
    Without validation: Reads system password file!
    With validation: Blocked because path escapes base directory

    HOW THIS FUNCTION PREVENTS ATTACKS:
     1. resolve() - Converts path to absolute form and follows symlinks
       - Before: "folder/../../../etc/passwd"
       - After: "/etc/passwd" (reveals the real location)

    2. is_relative_to() - Checks if resolved path is within base_dir
       - Safe: /home/user/downloads/file.txt is within /home/user/downloads
       - Unsafe: /etc/passwd is NOT within /home/user/downloads

    PATHLIB METHODS EXPLAINED:
    - path.resolve()
      * Converts relative paths to absolute
      * Resolves symbolic links (shortcuts/aliases to other files)
      * Removes . and .. components
      * Example: Path("~/downloads/../docs").resolve()
                 -> Path("/home/user/docs")

    - path.is_relative_to(base)
      * Python 3.9+ method
      * Returns True if path is under base directory
      * More reliable than string comparisons

    Args:
        path (Path): Path to validate (can be relative or absolute)
        base_dir (Optional[Path]): Base directory that path must be within.
                                   If None, only checks if path is valid.

    Returns:
        bool: True if path is safe to use, False if potentially dangerous

    Example usage:
        >>> base = Path("/home/user/downloads")
        >>> safe_path = Path("/home/user/downloads/file.txt")
        >>> dangerous_path = Path("/home/user/downloads/../../etc/passwd")
        >>>
        >>> validate_path(safe_path, base)  # True
        >>> validate_path(dangerous_path, base)  # False (escapes to /etc)
    """
