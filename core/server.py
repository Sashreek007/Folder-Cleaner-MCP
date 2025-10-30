"""
Server configuration and initialization
"""

from mcp.server.fastmcp import FastMCP


mcp = FastMCP(
    name="Folder Cleaner",
    instructions="""
I am a folder management assistant that helps you clean and organize directories.
    
    I can:
    - Find directories on your system (even with vague descriptions)
    - Remove duplicate files
    - Delete old files
    - Remove files by pattern (extensions, names)
    - Move files to different locations
    - Provide directory statistics
    
    I always confirm with you before performing destructive operations.

            """,
)
