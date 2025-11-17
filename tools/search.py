"""
Directory search and file listing handlers.

This module implements fuzzy directory search - the "magic" that lets users
type "clean downloads" and have the system find "home/path".

We use the Levenshtein distance algorithm (also called "edit distance"):
- It counts how many single-character edits are needed to transform one string into another
- Edits can be: insertions, deletions, substitutions
- Lower distance = closer match

Example:
"kitten" -> "sitting"
1. k->s (substitute)
2. e->i (substitute)
3. insert g at end
Distance = 3

The thefuzz library implements this efficiently and provides a scoring system (0-100).
"""

import os
from pathlib import Path
from typing import List, Dict
from thefuzz import fuzz, process

from core.server import mcp
