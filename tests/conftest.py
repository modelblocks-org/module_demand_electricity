"""Shared test fixtures."""

import os
from pathlib import Path
from urllib.request import urlretrieve

import pytest

TEST_FILES = {
    "EUROPE_S_C1_ADM1": "https://zenodo.org/records/20765043/files/EUROPE_S_C1_ADM1.parquet?download=1",
    "EUROPE_L_C34_ADM1": "https://zenodo.org/records/20765043/files/EUROPE_L_C34_ADM1.parquet?download=1",
}

TOKEN_ENTSOE = os.getenv("TOKEN_ENTSOE")
TOKEN_FILE = Path("resources/user/token_entsoe.txt")


@pytest.fixture(scope="session")
def user_path() -> Path:
    """Download and unzip test files."""
    user_dir = Path("resources/user/")
    # If test file have been downloaded, assume everything is OK.
    # Otherwise, re-download.
    for name, file_url in TEST_FILES.items():
        file_path = user_dir / name / "shapes.parquet"
        if not file_path.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
            urlretrieve(file_url, file_path)
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

    return TOKEN_FILE
