# Folder-Cleaner-MCP

A production-quality **Model Context Protocol (MCP) server** that enables Claude and other LLM applications to intelligently manage your file system. Search folders by fuzzy matching, detect duplicates, remove old files, and organize directories through natural conversation.

---

## Table of Contents

1. [What is This?](#what-is-this)
2. [Features](#features)
3. [Quick Start](#quick-start)
4. [Project Architecture](#project-architecture)
5. [Available Tools](#available-tools)
6. [Installation](#installation)
7. [Usage](#usage)
8. [Configuration](#configuration)
9. [Troubleshooting](#troubleshooting)
10. [Requirements](#requirements)

---

## What is This?

Folder-Cleaner-MCP is an MCP server that brings intelligent file management capabilities to Claude. Instead of manually organizing files or writing scripts, you can have natural conversations with Claude to clean, organize, and manage your directories.

### Example Conversation

```
You: "Clean my downloads folder"
Claude: [searches for downloads directory]
        I found your Downloads folder at /Users/you/Downloads
        It contains 1,247 files totaling 3.2 GB
        I detected 156 duplicate files using content hashing (1.1 GB)
        
        What would you like to do?

You: "Remove duplicates and files older than 1 year"
Claude: [analyzes files]
        I found 156 duplicate files and 89 files older than 1 year
        This will free up 2.3 GB total
        
        Should I proceed? (Files will be moved to trash)

You: "Yes"
Claude: Done! Moved 245 files to trash successfully.
        You can recover them from your Recycle Bin if needed.
```

### How It Works

MCP (Model Context Protocol) is an open standard that enables LLM applications to interact with external tools and data. This server exposes 13 file management tools that Claude can call through natural language, with all operations validated and previewed before execution for safety.

---

## Features

**Core Capabilities:**
- Fuzzy directory search - Find folders even with typos or partial names
- Intelligent file listing with multiple filters (extension, size, date, pattern)
- Duplicate file detection using SHA-256 content hashing
- Safe file deletion with trash/recycle bin (files remain recoverable)
- Batch file organization and movement
- Directory statistics and composition analysis
- All destructive operations require explicit confirmation

**Safety Features:**
- Input validation and path security
- Preview mode before any file operations
- Confirmation prompts for all deletions/moves
- Comprehensive error handling
- Files sent to trash instead of permanent deletion

---

## Quick Start

### Prerequisites
- Python 3.11 or higher
- `uv` package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR-USERNAME/Folder-Cleaner-MCP.git
cd Folder-Cleaner-MCP

# Install dependencies
uv pip install -r requirements.txt
```

### Run with MCP Inspector (Testing)

```bash
uv run mcp dev main.py
```

Then open http://localhost:5173 in your browser to test tools.

### Install in Claude Desktop

```bash
uv run mcp install main.py --name "Folder Cleaner"
```

Restart Claude Desktop and the "Folder Cleaner" server will appear in the MCP list.

### Direct Execution

```bash
python main.py
```

---

## Project Architecture

### File Structure

```
Folder-Cleaner-MCP/
├── main.py                    # Entry point - starts MCP server
├── requirements.txt           # Python dependencies
│
├── core/
│   ├── __init__.py
│   └── server.py             # FastMCP server setup and configuration
│
├── handlers/                  # Tool implementations
│   ├── __init__.py
│   ├── search.py             # Directory search and file listing (3 tools)
│   ├── duplicate.py          # Duplicate detection (2 tools)
│   ├── cleanup.py            # File deletion operations (4 tools)
│   └── move.py               # File moving and organization (4 tools)
│
└── utils/
    ├── __init__.py
    ├── file_ops.py           # File system operations
    └── validators.py         # Input validation and security
```

### Architecture Overview

The project follows a modular architecture:

- **core/** - MCP server setup and FastMCP initialization
- **handlers/** - Tool implementations organized by category
- **utils/** - Shared utilities for file operations and validation
- **main.py** - Entry point that starts the server

---

## Available Tools

### Search Tools (3 tools)

**search_directory(query, search_base)**
- Finds directories matching user's description using fuzzy matching
- Returns ranked matches with similarity scores
- Example: "downloads" finds "/Users/you/Downloads"

**list_files(directory, extension, min_size_mb, older_than_days)**
- Lists files in a directory with optional filters
- Supports filtering by extension, minimum size, and age
- Returns file metadata including sizes and modification dates

**get_directory_stats(directory)**
- Returns comprehensive directory statistics
- Provides total file count, total size, and file type breakdown
- Useful for understanding directory composition

### Duplicate Detection (2 tools)

**find_duplicates(directory, include_subdirs)**
- Identifies duplicate files using SHA-256 content hashing
- Works recursively through subdirectories if enabled
- Returns groups of identical files with total space wasted

**preview_duplicate_removal(duplicate_hash)**
- Shows which files would be kept/deleted for a duplicate group
- Allows user to confirm before removal
- Returns space that would be freed

### File Cleanup (4 tools)

**delete_by_pattern(directory, pattern)**
- Deletes files matching a pattern (extension, name, keyword)
- Moves files to trash instead of permanent deletion
- Returns count of files deleted

**delete_oldest_files(directory, days)**
- Removes files older than specified number of days
- Preserves recent files automatically
- Returns list of deleted files

**delete_by_size(directory, min_size_mb)**
- Deletes files larger than specified size threshold
- Useful for removing large unnecessary files
- Returns freed space in MB

**get_trash_status()**
- Shows current trash/recycle bin usage
- Helps users understand available recovery options
- Returns trash location and size

### File Organization (4 tools)

**move_by_extension(source, destination)**
- Organizes files by extension into separate directories
- Creates folders for each file type found
- Example: Moves all .pdf files to destination/pdf/

**move_by_date(source, destination)**
- Organizes files into folders by creation/modification date
- Default structure: YYYY/Month/
- Example: Old files go to destination/2020/January/

**move_by_pattern(source, destination, pattern)**
- Moves files matching a pattern to destination
- Supports wildcard patterns and multiple criteria
- Example: Move all files starting with "backup_"

**move_largest_files(source, destination, count)**
- Moves the N largest files from source to destination
- Useful for freeing up space in full directories
- Returns total space freed

---

## Installation

### Dependencies

The project requires:
- `mcp` - Official MCP Python SDK (protocol handling)
- `pydantic` - Data validation using Python type annotations
- `fuzzywuzzy` - Fuzzy string matching for directory search
- `send2trash` - Cross-platform trash/recycle bin support
- `python-Levenshtein` - Optional performance improvement for fuzzy matching

### Install via UV

```bash
uv pip install -r requirements.txt
```

### Install via PIP

```bash
pip install -r requirements.txt
```

---

## Usage

### Via Claude Desktop

1. Install in Claude Desktop (see Quick Start section)
2. Start a conversation with Claude
3. Ask Claude to help with file management:
   - "Find and remove duplicate files in my downloads"
   - "Show me what's taking up space"
   - "Organize my documents by date"
   - "Move all large files somewhere else"

### Via MCP Inspector

1. Run `uv run mcp dev main.py`
2. Open http://localhost:5173
3. Select tools and test with parameters
4. Useful for debugging and testing individual tools

### Via Command Line

```bash
python main.py
```

---

## Configuration

### Server Name and Version

Edit `core/server.py` to customize server identity:

```python
mcp = FastMCP(
    name="Folder Cleaner",
    version="1.0.0"
)
```

### Tool Parameters

Each tool accepts different parameters. See Available Tools section for detailed parameters for each tool.

---

## Troubleshooting

### Issue: "Module not found" errors

**Solution:** Reinstall dependencies
```bash
uv pip install -r requirements.txt --force-reinstall
```

### Issue: "Permission denied" when deleting files

**Causes:**
- File is open in another application
- File or directory is read-only
- Insufficient permissions for directory

**Solution:** Close the file or change permissions

### Issue: Fuzzy search finds wrong directories

**Cause:** Search threshold may be too permissive

**Solution:** The top result is always the best match. Verify suggestions before confirming.

### Issue: Duplicate detection is slow on large directories

**Cause:** Hashing many large files takes time

**Solution:** This is expected behavior with large operations. They may take several seconds.

### Issue: "Resource temporarily unavailable"

**Cause:** File system is busy or file permissions changed during operation

**Solution:** Try the operation again or check file permissions

### Issue: Cannot access home directory

**Cause:** Path expansion failed or permissions issue

**Solution:** 
- Check that `~` expands correctly: `echo ~`
- Verify directory permissions: `ls -ld ~`

### Issue: Server won't start

**Causes:**
- Port already in use (for HTTP transport)
- Python version incompatibility
- Missing dependencies

**Solution:**
- Check Python version: `python --version` (need 3.11+)
- Reinstall dependencies
- Kill any existing server processes

---

## Requirements

### System Requirements
- Python 3.11 or higher
- 100 MB disk space for installation
- Read/write access to directories being managed

### Supported Platforms
- macOS (10.14+)
- Linux (Ubuntu 18.04+, Debian 10+, Fedora 30+)
- Windows (10/11 with WSL2 or native Python)

### Python Dependencies

```
mcp>=1.1.0
pydantic>=2.0.0
fuzzywuzzy>=0.18.0
send2trash>=1.8.0
python-Levenshtein>=0.21.0
```

---

## Safety Considerations

### File Operations

- All deletions move files to trash/recycle bin (recoverable)
- No permanent deletion without explicit user confirmation
- Files are previewed before operations
- Path validation prevents access outside intended directories

### Security

- Input validation on all parameters
- Path traversal attack prevention
- Symlink handling
- No remote code execution possible

### Data Protection

- Read-only operations (search, list, stats) never modify files
- Destructive operations always require confirmation before execution
- Operation results logged for verification

---

## Contributing

To extend this project with new tools:

1. Create new tool in appropriate handler file (or create new handler)
2. Use `@mcp.tool()` decorator to register
3. Include comprehensive docstrings for all parameters
4. Test with MCP Inspector
5. Update this README with new tool documentation

Example of adding a tool:

```python
@mcp.tool()
def new_tool(directory: str, parameter: str) -> dict:
    """Description of what this tool does."""
    # Implementation
    return {"result": "..."}
```

---

## License

MIT License - Use freely in your projects and modify as needed.

---

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review handler source code for implementation details
3. Test with MCP Inspector for debugging
4. Verify file permissions and paths

---

## Related Resources

- Model Context Protocol: https://modelcontextprotocol.io
- FastMCP: https://github.com/jlowin/fastmcp
- MCP Python SDK: https://github.com/modelcontextprotocol/python-sdk
- Python pathlib: https://docs.python.org/3/library/pathlib.html
