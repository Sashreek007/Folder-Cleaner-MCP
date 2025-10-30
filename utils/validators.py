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


def validate_filename(filename: str) -> bool:
    """
        Check if a filename is safe to use.

        Args:
        filename (str): The filename to validate (not full path, just name)

    Returns:
        bool: True if filename is safe, False if it contains dangerous patterns

    Example usage:
        >>> validate_filename("report.txt")  # True
        >>> validate_filename("../etc/passwd")  # False
        >>> validate_filename("CON")  # False (Windows reserved)
        >>> validate_filename("file\x00.txt")  # False (null byte)
    """

    if not filename:
        return False

    if "/" in filename or "//" in filename:
        return False

    if filename in [".", ".."]:
        return False
    if "\x00" in filename:
        return False
    # check for windows reserved words
    windows_reserved = [
        "CON",
        "PRN",
        "AUX",
        "NUL",  # DOS device names
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",  # Serial ports
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",  # Parallel ports
    ]

    nameWithoutExt = filename.split(".")[0].upper()

    if nameWithoutExt in windowsReserved:
        return False

    if any(ord(char) < 32 for char in filename):
        return False

    return True
