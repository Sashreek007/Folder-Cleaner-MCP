"""
Main entry point for the Folder Cleaner MCP Server.
"""

import sys
import logging

from core.server import mcp

import handlers


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)


logger = logging.getLogger(__name__)
# __name__ is the module name


def main():
    """
    Main function that starts the MCP server.

    This is called when the script is run directly
    """
    logger.info("Starting Folder Cleaner MCP Server...")
    try:
        logger.info("Server is ready and waiting for connections...")
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
        sys.exit(0)

    except Exception as e:
        logger.error(f"Server crashed with error: {str(e)}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
