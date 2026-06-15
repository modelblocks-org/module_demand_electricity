"""Tests to be executed locally, as they are more computationally intense."""

import subprocess


def test_europe_nuts2(user_path):
    """Test that the Europe NUTS2 shapes are correct."""
    target = "results/demand_electricity_Europe_NUTS2_MW.parquet"
    assert subprocess.run(
        f"snakemake --use-conda --cores 4 --forceall {target}",
        shell=True,
        check=True,
        cwd=user_path.parent.parent,
    )
