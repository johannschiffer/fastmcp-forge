"""
FastMCP Forge CLI and built-in MCP Server.
Commands:
  fastmcp-forge new my-server
  fastmcp-forge validate ./my-server
  fastmcp-forge serve
When launched without arguments over a non-TTY pipe (e.g. uvx fastmcp-forge in an MCP client),
starts the built-in FastMCP Forge stdio MCP server automatically.
"""
import argparse
import json
import sys
from typing import Any, Dict

from . import __version__
from .scaffolder import ProjectScaffolder
from .server import FastMCP


def build_forge_mcp_server() -> FastMCP:
    """Create the built-in FastMCP Forge MCP server exposing scaffolding and validation tools."""
    app = FastMCP(
        name="fastmcp-forge",
        version=__version__,
        description="MCP server scaffolder and project validator",
    )

    @app.tool(description="Scaffold a new FastMCP server project with tests and configuration")
    def scaffold_project(project_name: str, target_dir: str = ".") -> Dict[str, Any]:
        return ProjectScaffolder.create_project(project_name, target_dir=target_dir)

    @app.tool(description="Validate an existing FastMCP project directory for syntax and structure")
    def validate_project(project_dir: str) -> Dict[str, Any]:
        return ProjectScaffolder.validate_project(project_dir)

    return app


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="fastmcp-forge",
        description="FastMCP Forge: framework, CLI code generator, and MCP server for scaffolding MCP projects",
    )
    parser.add_argument("-v", "--version", action="version", version=f"fastmcp-forge {__version__}")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    new_parser = subparsers.add_parser("new", help="Scaffold a new FastMCP server project")
    new_parser.add_argument("name", help="Project name (e.g. 'analytics-mcp')")
    new_parser.add_argument("--dir", default=".", help="Target directory (default: current directory)")

    val_parser = subparsers.add_parser("validate", help="Validate a scaffolded FastMCP project directory")
    val_parser.add_argument("path", help="Project directory path")

    subparsers.add_parser("serve", help="Run FastMCP Forge as a stdio MCP server")

    args = parser.parse_args()

    if args.command == "new":
        try:
            res = ProjectScaffolder.create_project(args.name, target_dir=args.dir)
        except ValueError as exc:
            print(f"[ERROR] {exc}", file=sys.stderr)
            sys.exit(2)
        print(f"[OK] Created new FastMCP project '{res['project_name']}' at: {res['path']}")
        print("Generated files:")
        for f in res["files"]:
            print(f"  - {f}")
        print("\nNext steps:")
        print(f"  cd {res['project_name']}")
        print("  pip install -r requirements.txt")
        print("  pytest tests/")
    elif args.command == "validate":
        res = ProjectScaffolder.validate_project(args.path)
        print(json.dumps(res, indent=2))
        if not res["valid"]:
            sys.exit(1)
    elif args.command == "serve":
        build_forge_mcp_server().run_stdio()
    else:
        if not sys.stdin.isatty():
            build_forge_mcp_server().run_stdio()
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
