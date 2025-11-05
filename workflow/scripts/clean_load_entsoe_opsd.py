"""Clean load data from ENTSO-E."""

import logging

import matplotlib.pyplot as plt
import pandas as pd
import yaml
from _plots import plot_missing_values_heatmap, plot_national_profiles
from _schemas import LoadENTSOE

logger = logging.getLogger(__name__)


def load_yaml(path):
    """Load a YAML file."""
    with open(path) as file:
        return yaml.safe_load(file)


def main(
    path_raw_load,
    path_map_countries,
    output_load,
    output_plot_missing,
    output_plot_profiles,
):
    """Clean ENTSO-E load data (units of MW), downloaded from open power system data (OPSD)."""
    load = pd.read_csv(path_raw_load)
    load = LoadENTSOE.validate(load)
    map_alpha_2_to_alpha_3 = load_yaml(path_map_countries)

    load = load.loc[load["variable"] == "load"]
    load = load.loc[load["attribute"] == "actual_entsoe_power_statistics"]

    load_alpha3 = load.loc[load["region"].isin(map_alpha_2_to_alpha_3.keys())]
    load_alpha3.loc[:, "region"] = load_alpha3.loc[:, "region"].map(
        map_alpha_2_to_alpha_3
    )

    load_pivot = pd.pivot(
        load_alpha3, index=["utc_timestamp"], columns=["region"], values="data"
    )
    load_pivot.index = pd.to_datetime(load_pivot.index).tz_localize(None)

    load_pivot.to_parquet(output_load)

    plot_missing_values_heatmap(load_pivot)
    plt.savefig(output_plot_missing, bbox_inches="tight", dpi=300)

    plot_national_profiles(load_pivot)
    plt.savefig(output_plot_profiles, bbox_inches="tight", dpi=300)


if __name__ == "__main__":
    main(
        path_raw_load=snakemake.input.load,
        path_map_countries=snakemake.input.map_countries,
        output_load=snakemake.output.load,
        output_plot_missing=snakemake.output.plot_missing,
        output_plot_profiles=snakemake.output.plot_profiles,
    )
