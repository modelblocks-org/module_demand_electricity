"""Clean load data from ENTSO-E."""

import logging

import matplotlib.pyplot as plt
import pandas as pd
import pycountry
from _plots import plot_missing_values_heatmap, plot_national_profiles
from _schemas import LoadENTSOE

logger = logging.getLogger(__name__)


def get_map_alpha2_to_alpha3(countries_alpha_2):
    """Get mapping from alpha-2 to alpha-3 country codes."""
    map_alpha2_to_alpha3 = {}
    for alpha2 in countries_alpha_2:
        country = pycountry.countries.get(alpha_2=alpha2)
        if country is not None:
            map_alpha2_to_alpha3[alpha2] = country.alpha_3
        else:
            logger.warning(
                f"Country with alpha-2 code '{alpha2}' not found in pycountry."
            )

    return map_alpha2_to_alpha3


def main(path_raw_load, output_load, output_plot_missing, output_plot_profiles):
    """Clean ENTSO-E load data (units of MW), downloaded from open power system data (OPSD)."""
    load = pd.read_csv(path_raw_load)
    load = LoadENTSOE.validate(load)

    load = load.loc[load["variable"] == "load"]
    load = load.loc[load["attribute"] == "actual_entsoe_power_statistics"]

    map_alpha2_to_alpha3 = get_map_alpha2_to_alpha3(load["region"].unique())

    load = load.loc[load["region"].isin(map_alpha2_to_alpha3.keys())]
    load.loc[:, "region"] = load.loc[:, "region"].map(map_alpha2_to_alpha3)

    load_pivot = pd.pivot(
        load, index=["utc_timestamp"], columns=["region"], values="data"
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
        output_load=snakemake.output.load,
        output_plot_missing=snakemake.output.plot_missing,
        output_plot_profiles=snakemake.output.plot_profiles,
    )
