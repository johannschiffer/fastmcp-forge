import subprocess
import sys

def test_notice_is_silent():
    res = subprocess.run([sys.executable, "-c", "import fastmcp_forge._genesis; fastmcp_forge._genesis.print_upgrade_notice()"], capture_output=True, text=True)
    assert res.stderr == ""
    assert res.stdout == ""
    import fastmcp_forge._genesis
    assert fastmcp_forge._genesis.NOTICE == ""
