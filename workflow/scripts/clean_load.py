"""Clean load data from ENTSO-E."""

import logging

import pandas as pd
import pycountry

logger = logging.getLogger(__name__)


def map_to_iso_countries(countries_alpha_2):
    """Map ISO 3166-1 alpha-2 country codes to alpha-3 codes."""
    map_alpha_2_to_alpha_3 = {
        alpha_2: pycountry.countries.get(alpha_2=alpha_2)
        for alpha_2 in countries_alpha_2
    }
    not_found = [
        alpha_2 for alpha_2, cntr in map_alpha_2_to_alpha_3.items() if cntr is None
    ]
    logger.info("Countries not found in pycountry are dropped:", not_found)
    map_alpha_2_to_alpha_3 = {
        alpha_2: cntr.alpha_3
        for alpha_2, cntr in map_alpha_2_to_alpha_3.items()
        if cntr is not None
    }
    return map_alpha_2_to_alpha_3


def main(path_raw_load, path_output_load):
    """Main function."""
    load = pd.read_csv(path_raw_load)

    load = load.loc[load["variable"] == "load"]
    load = load.loc[load["attribute"] == "actual_entsoe_power_statistics"]

    countries = load.region.unique()
    map_alpha_2_to_alpha_3 = map_to_iso_countries(countries)

    load_alpha3 = load.loc[load["region"].isin(map_alpha_2_to_alpha_3.keys())]
    load_alpha3["region"] = load_alpha3["region"].map(map_alpha_2_to_alpha_3)

    load_pivot = pd.pivot(
        load_alpha3, index=["utc_timestamp"], columns=["region"], values="data"
    )
    load_pivot.index = pd.to_datetime(load_pivot.index)

    load_pivot = load_pivot.to_parquet(path_output_load)


if __name__ == "__main__":
    main(snakemake.input[0], snakemake.output[0])
