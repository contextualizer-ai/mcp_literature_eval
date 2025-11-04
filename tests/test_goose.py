# Test Goose temporary environment.
#
# To run:
# uv run pytest tests/test_goose.py
#
# To print out paths and extensions:
# uv run pytest --log-cli-level=INFO tests/test_goose.py
#
# To print full goose info -v, use:
# uv run pytest --log-cli-level=DEBUG tests/test_goose.py
#
# tests/test_goose.py
from __future__ import annotations
import logging
import os
import platform
import re
import shutil
import subprocess
from pathlib import Path

import pytest
import yaml

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)  # or adjust logging here

HEADER_RE = re.compile(r"^Goose (Version|Locations|Configuration):\s*$", re.M)
LOC_LINE_RE = re.compile(r"^\s*Config file:\s*(?P<path>.+?)\s*$", re.M)


@pytest.mark.parametrize(
    "cmd",
    [
        ["goose", "--version"],
        # ["goose", "info", "-v"],
        [
            "goose",
            "run",
            "-t",
            "What is the first sentence of section 2 in PMID:28027860?",
        ],
    ],
)
def test_goose_reads_config_from_temp_dir(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, cmd
):
    is_windows = platform.system().lower().startswith("win")

    goose_path = shutil.which("goose")
    logger.info("Using goose at: %s", goose_path or "(not found on PATH)")

    # 1) Redirect config home
    if is_windows:
        monkeypatch.setenv("APPDATA", str(tmp_path))
        config_dir = tmp_path / "Block" / "goose" / "config"
        data_dir = tmp_path / "Block" / "goose" / "data"
    else:
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        config_dir = tmp_path / "goose"
        data_dir = tmp_path / "goose"

    config_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)

    # 2) Minimal config
    config_path = config_dir / "config.yaml"
    cfg = {"providers": {}, "extensions": {}, "keyring": {"enabled": False}}
    config_path.write_text(yaml.safe_dump(cfg, sort_keys=False), encoding="utf-8")
    logger.info("Wrote temp Goose config: %s", config_path)

    # 3) Harden env
    env = os.environ.copy()
    env["GOOSE_DISABLE_KEYRING"] = "1"

    # 4) Run Goose
    proc = subprocess.run(
        cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )

    # 5) Assertions
    if cmd == ["goose", "--version"]:
        assert proc.returncode == 0, f"Unexpected failure: {proc.stderr}"
        assert proc.stdout.strip(), "Expected version string"

    if cmd == ["goose", "info", "-v"]:
        assert proc.returncode == 0, f"'goose info -v' failed: {proc.stderr}"

        # A) Verify the reported config path from the Locations block
        m = LOC_LINE_RE.search(proc.stdout)
        assert m, f"Could not find 'Config file:' line in output:\n{proc.stdout}"
        reported = Path(m.group("path")).resolve()
        assert reported == config_path.resolve(), (
            f"Expected Goose to use temp config {config_path}, but it reported {reported}"
        )

        # B) Parse YAML config block robustly:
        #    If the whole output is YAML (as your current version suggests), we can load directly.
        #    If a future version mixes prose, fall back to extracting from the 'Goose Configuration' section.
        parsed = None
        try:
            parsed = yaml.safe_load(proc.stdout)
        except Exception as e:
            raise AssertionError(
                f"Could not parse YAML from 'goose info -v': {e}"
            ) from e

        assert isinstance(parsed, dict), "Expected YAML mapping from 'goose info -v'"
        cfg_root = parsed.get("Goose Configuration", parsed)
        assert isinstance(cfg_root, dict), (
            "Expected 'Goose Configuration' to be a mapping"
        )

        ext_cfg = cfg_root.get("extensions") or {}
        assert isinstance(ext_cfg, dict), "Expected 'extensions' to be a mapping"
        enabled_exts = [
            n
            for n, c in ext_cfg.items()
            if isinstance(c, dict) and c.get("enabled", True)
        ]
        logger.info(
            "Extensions found: %s", sorted(ext_cfg.keys()) if ext_cfg else "(none)"
        )
        logger.info(
            "Enabled extensions: %s", enabled_exts if enabled_exts else "(none)"
        )
        assert not enabled_exts, f"Extensions still enabled: {enabled_exts}"

        # Full dump at DEBUG for easy inspection
        logger.debug("\n---\ngoose info -v\n\n%s\n---", proc.stdout.rstrip())

    if proc.returncode != 0:
        print("'%s' exited with code %s", " ".join(cmd), proc.returncode)
        print("CMD:", cmd)
        print("STDOUT:", proc.stdout)
        print("STDERR:", proc.stderr)
