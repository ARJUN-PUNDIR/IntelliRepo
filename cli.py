import argparse
import sys
from core.logger import setup_logger

logger = setup_logger("intellirepo.cli")

def main():
    """
    The Front Door of IntelliRepo.
    Parses command line arguments and routes them to the correct system.
    """
    parser = argparse.ArgumentParser(
        description="IntelliRepo: The Autonomous Multi-Agent Software Engineering System"
    )
    
    # We create "subcommands" so the tool can do multiple things
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Command 1: solve
    solve_parser = subparsers.add_parser("solve", help="Ask the AI Agents to solve a GitHub Issue.")
    solve_parser.add_argument(
        "--url", 
        required=True, 
        help="The full URL to the GitHub Issue (e.g., https://github.com/IntelliRepo/demo/issues/42)"
    )
    
    # Command 2: build-brain (Useful for regenerating the Neo4j/Chroma databases)
    build_parser = subparsers.add_parser("build-brain", help="Rebuild the Graph and Vector databases from scratch.")
    
    # Command 3: start-mcp (Useful for debugging the switchboards)
    mcp_parser = subparsers.add_parser("start-mcp", help="Start the FastMCP servers manually.")

    # Parse what the user typed in the terminal
    args = parser.parse_args()

    if args.command == "solve":
        logger.info(f"CLI routing 'solve' command for URL: {args.url}")
        # (We will link this to the Orchestrator in the next lecture!)
        print(f"🚀 Preparing to solve: {args.url}")
        
    elif args.command == "build-brain":
        logger.info("CLI routing 'build-brain' command.")
        print("🧠 Building the Dual-Brain... (Mock)")
        
    elif args.command == "start-mcp":
        logger.info("CLI routing 'start-mcp' command.")
        print("🔌 Starting MCP Switchboards... (Mock)")
        
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
