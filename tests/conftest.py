"""Shared test fixtures."""

import os
import shutil
import zipfile
from pathlib import Path
from urllib.request import urlretrieve

import pytest

TEST_FILES = (
    "https://surfdrive.surf.nl/public.php/dav/files/nHZmPGBibmsWDrH/?accept=zip"
)

TOKEN_ENTSOE = os.getenv("TOKEN_ENTSOE")
TOKEN_FILE = Path("resources/user/token_entsoe.txt")


@pytest.fixture(scope="session")
def user_path() -> Path:
    """Download and unzip test files."""
    user_dir = Path("resources/user/")
    # If test suite has been downloaded, assume everything is OK.
    # Otherwise, cleanup and re-download.
    if not Path(user_dir / "module_demand_electricity_files.zip").exists():
        shutil.rmtree(user_dir, ignore_errors=True)
        Path(user_dir).mkdir(parents=True, exist_ok=True)
        test_zip = Path(user_dir / "module_demand_electricity_files.zip")
        urlretrieve(TEST_FILES, test_zip)
        with zipfile.ZipFile(test_zip, "r") as zfile:
            zfile.extractall(user_dir)
    return user_dir


@pytest.fixture
def token_entsoe():
    """Fixture to get token_entsoe.txt in CI.

    If an environment variable `TOKEN_ENTSOE` is set,
    and if token_entsoe.txt is not present or empty,
    write the token to the file.
    """
    if TOKEN_ENTSOE and not TOKEN_FILE.exists() or TOKEN_FILE.read_text().strip() == "":
        TOKEN_FILE.write_text(TOKEN_ENTSOE)
