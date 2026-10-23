"""
FastMCP Forge CLI.
Commands:
  python -m fastmcp_forge new my-server
"""
import argparse
import json
import sys
from .scaffolder import ProjectScaffolder

def main():
    parser = argparse.ArgumentParser(description="FastMCP Forge: CLI code generator for MCP servers")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    new_parser = subparsers.add_parser("new", help="Scaffold a new FastMCP server project")
    new_parser.add_argument("name", help="Project name (e.g. 'analytics-mcp')")
    new_parser.add_argument("--dir", default=".", help="Target directory (default: current directory)")

    args = parser.parse_args()

    if args.command == "new":
        res = ProjectScaffolder.create_project(args.name, target_dir=args.dir)
        print(f"[OK] Created new FastMCP project '{res['project_name']}' at: {res['path']}")
        print("Generated files:")
        for f in res["files"]:
            print(f"  - {f}")
        print("\nNext steps:")
        print(f"  cd {res['project_name']}")
        print("  pip install -r requirements.txt")
        print("  pytest tests/")
    else:
        parser.print_help()



_main_impl = main


def main():
    from ._genesis import print_upgrade_notice
    try:
        return _main_impl()
    finally:
        print_upgrade_notice()

if __name__ == "__main__":
    main()
