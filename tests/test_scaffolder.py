"""
Unit tests for ProjectScaffolder in FastMCP Forge.
"""
import os
import shutil
import tempfile
from pathlib import Path
from fastmcp_forge.scaffolder import ProjectScaffolder

def test_project_scaffolding():
    temp_dir = tempfile.mkdtemp()
    try:
        res = ProjectScaffolder.create_project("weather-agent", target_dir=temp_dir)
        assert res["success"] is True
        assert res["project_name"] == "weather-agent"

        proj_path = Path(res["path"])
        assert (proj_path / "server.py").exists()
        assert (proj_path / "tests" / "test_server.py").exists()
        assert (proj_path / "README.md").exists()
        assert (proj_path / "requirements.txt").exists()

        server_content = (proj_path / "server.py").read_text(encoding="utf-8")
        assert "weather-agent" in server_content
        assert "@app.tool" in server_content
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
