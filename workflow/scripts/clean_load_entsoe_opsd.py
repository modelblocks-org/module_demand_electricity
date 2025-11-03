"""Clean load data from ENTSO-E."""

import logging

import matplotlib.pyplot as plt
import pandas as pd
import yaml
from _plots import plot_missing_values_heatmap

logger = logging.getLogger(__name__)


def load_yaml(path):
    """Load a YAML file."""
    with open(path) as file:
        return yaml.safe_load(file)


def main(path_raw_load, path_map_countries, path_output_load, path_output_plot):
    """Main function."""
    load = pd.read_csv(path_raw_load)
    map_alpha_2_to_alpha_3 = load_yaml(path_map_countries)

    load = load.loc[load["variable"] == "load"]
    load = load.loc[load["attribute"] == "actual_entsoe_power_statistics"]

    load_alpha3 = load.loc[load["region"].isin(map_alpha_2_to_alpha_3.keys())]
    load_alpha3["region"] = load_alpha3["region"].map(map_alpha_2_to_alpha_3)

    load_pivot = pd.pivot(
        load_alpha3, index=["utc_timestamp"], columns=["region"], values="data"
    )
    load_pivot.index = pd.to_datetime(load_pivot.index).tz_localize(None)

    load_pivot.to_parquet(path_output_load)

    plot_missing_values_heatmap(load_pivot)
    plt.savefig(path_output_plot, bbox_inches="tight", dpi=300)


if __name__ == "__main__":
    main(
        snakemake.input.load,
        snakemake.input.map_countries,
        snakemake.output.load,
        snakemake.output.plot,
    )
