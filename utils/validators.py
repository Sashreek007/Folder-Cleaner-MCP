"""
    Input validation utilites for MCP Folder Cleaner.
This module provides security-critical validation functions to prevent:
- Directory traversal attacks (accessing files outside allowed directories)
- Invalid filenames that could crash or exploit the system
- Pattern injection attacks
"""

import re
from pathlib import Path
from typing import Optional
import platform


def validateDirectoryPath(pathStr: str, base_dir: Optional[Path] = None) -> Path:
    """
        Validate and convert a directory path string to a Path object.
    This ensures:
        - The path is not empty
        - The path exists
        - The path is actually a directory
        - The path is accessible i.e having permissions
    Args:
        pathStr: String representation of dir path
    Returns:
        Path object representing the validated directory
    Raises:
        ValueError
    """
    if not pathStr or not pathStr.strip():
        raise ValueError("directory path cannot be empty")

    path = Path(pathStr).expanduser()

    try:
        path = path.resolve()
    except (RuntimeError, OSError) as e:
        raise ValueError(f"Invalid path: {pathStr}. Error: {str(e)}")
    if base_dir and not validate_path(path, base_dir):
        raise ValueError(
            f"Security violation: Path '{path}' is outside allowed "
            f"base directory '{base_dir.resolve()}'"
        )

    if not path.exists():
        raise ValueError(f"Directory does not exist : {path}")

    if not path.is_dir():
        raise ValueError(f"Path exists but is not a directory: {path}")

    try:
        next(path.iterdir(), None)

    except PermissionError:
        raise ValueError(f"Permission denied: Cannot access directory {path}")
    except StopIteration:
        pass
    return path


def validate_path(path: Path, base_dir: Optional[Path] = None) -> bool:
    """
        Validate that a path is safe to operate on.

        This prevents directory traversal attacks and accidental system file operations.
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

    try:
        resolved_path = path.resolve()

        if base_dir:
            base_dir = base_dir.resolve()

            return resolved_path.is_relative_to(base_dir)
        return True
    except (ValueError, RuntimeError, OSError) as e:
        return False
