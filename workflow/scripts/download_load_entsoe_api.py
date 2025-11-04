"""Download electricity load data from ENTSO-E using the entsoe-py library."""

import logging

import matplotlib.pyplot as plt
import pandas as pd
import yaml
from _plots import plot_missing_values_heatmap
from entsoe import EntsoePandasClient
from entsoe.exceptions import NoMatchingDataError

logger = logging.getLogger(__name__)


def load_txt(filepath):
    """Load text file."""
    with open(filepath) as file:
        data = file.read()
    return data


def load_yaml(path):
    """Load a YAML file."""
    with open(path) as file:
        return yaml.safe_load(file)


def main(start, end, country_codes, token, output_load, output_plot):
    """Download load in MW via the ENTSO-E API."""
    start = pd.Timestamp(start, tz="UTC")
    end = pd.Timestamp(end, tz="UTC")
    country_codes = load_yaml(country_codes)
    token = load_txt(token)
    client = EntsoePandasClient(api_key=token)

    data = []
    for country_alpha_2, country_alpha_3 in country_codes.items():
        logger.info(f"Downloading data for {country_alpha_2} from {start} to {end}")
        try:
            df_country = client.query_load(
                country_code=country_alpha_2, start=start, end=end
            )
            df_country = df_country["Actual Load"]
            df_country.name = country_alpha_3

        except NoMatchingDataError:
            logger.warning(
                f"No data found for {country_alpha_2}/{country_alpha_3} in the given period: {start} to {end}"
            )
            df_country = pd.Series(name=country_alpha_3)

        data.append(df_country)

    df = pd.concat(data, axis=1)

    df.index = pd.to_datetime(df.index, utc=True)

    df = df.resample("1H").mean()

    df.to_parquet(output_load)

    plot_missing_values_heatmap(df)
    plt.savefig(output_plot, bbox_inches="tight", dpi=300)


if __name__ == "__main__":
    main(
        start=snakemake.config["temporal_scope"]["start"],
        end=snakemake.config["temporal_scope"]["end"],
        country_codes=snakemake.input.country_codes_entsoe,
        token=snakemake.input.token_entsoe,
        output_load=snakemake.output.load,
        output_plot=snakemake.output.plot,
    )
