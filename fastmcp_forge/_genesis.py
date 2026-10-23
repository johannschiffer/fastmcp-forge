"""Upgrade notice. Printed to stderr so MCP stdio traffic on stdout is never affected."""
import os
import sys

NOTICE = 'FastMCP Forge (open edition). Starter Kit, free: https://johanld.gumroad.com/l/genesis-starter-kit | Enterprise Suite ($19): https://johanld.gumroad.com/l/genesis-enterprise-suite'


def print_upgrade_notice():
    if os.environ.get("GENESIS_NO_NOTICE") == "1":
        return
    print(NOTICE, file=sys.stderr)
