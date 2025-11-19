"""Duty definitions for the project."""

from __future__ import annotations

import sys
from pathlib import Path

from duty import duty

PY_SRC_PATHS = (Path(_) for _ in ("src", "tests", "duties.py"))
PY_SRC_LIST = tuple(str(_) for _ in PY_SRC_PATHS)
PY_SRC = " ".join(PY_SRC_LIST)
TEST_TMP_PATH = Path("tmp")
TEST_COV_PATH = TEST_TMP_PATH / "coverage"
CI_TEST_PARALLEL = 4


@duty
def clean(ctx):
    """Clean cache and temporary files."""
    ctx.run("rm -rf .coverage*")
    ctx.run("rm -rf .pytest_cache")
    ctx.run("rm -rf .ruff_cache")
    ctx.run("rm -rf tests/.pytest_cache")
    ctx.run("rm -rf tests/.ruff_cache")
    ctx.run("rm -rf build")
    ctx.run("rm -rf dist")
    ctx.run("rm -rf *.egg-info")
    ctx.run("rm -rf coverage.xml")
    ctx.run("find . -type d -name __pycache__ -exec rm -rf {} +")
    ctx.run("find . -name '*.pyc' -delete")


@duty(pre=["clean"])
def install(ctx):
    """Install dependencies."""
    ctx.run("uv pip install -e .")


@duty
def install_dev(ctx):
    """Install dev dependencies."""
    ctx.run("uv pip install -e '.[dev]'")


@duty
def lint(ctx):
    """Lint and format the code."""
    ctx.run(f"ruff check {PY_SRC}", title="Checking code with ruff")
    ctx.run(f"ruff format {PY_SRC}", title="Formatting code with ruff")


@duty
def test(ctx, match: str = ""):
    """Run tests."""
    py_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    title = f"Running tests on Python {py_version}"
    marker = f"-m '{match}'" if match else ""
    ctx.run(
        f"pytest -n {CI_TEST_PARALLEL} {marker} --cov=src --cov-report=xml",
        title=title,
    )


@duty
def run_notebook(ctx, path: str = "notebooks/usage_example.py"):
    """Run a notebook."""
    ctx.run(f"marimo run {path}", pty=True)


@duty
def bump_version(ctx, part: str):
    """Bump the version of the project."""
    ctx.run(f"bump-my-version bump {part}", title=f"Bumping version {part}")
