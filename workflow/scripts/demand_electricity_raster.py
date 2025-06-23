"""Prepare electricity demand timeseries at raster resolution."""

import logging

import geopandas as gpd
import gregor
import matplotlib.pyplot as plt
import pandas as pd
import rioxarray as rxr


def plot_profiles(profiles):
    """Plot electricity demand profiles."""
    fig, ax = plt.subplots(figsize=(10, 6))

    return fig


def plot_map(shapes, demand):
    """Plot annual electricity demand on a map."""
    fig, ax = plt.subplots(figsize=(10, 10))

    return fig


def main(
    path_demand,
    path_population,
    path_countries,
    path_output_data,
    path_output_plot,
    path_output_map,
):
    """Main function."""
    demand = pd.read_parquet(path_demand)
    countries = gpd.read_file(path_countries)
    countries = countries.set_index(countries.columns[0])
    population = rxr.open_rasterio(path_population)
    population = population.sel(band=1)

    # match load data with countries
    regions = demand.columns
    missing_countries = set(regions).difference(countries["id"].unique())
    logger.info("Drop timeseries for missing countries", missing_countries)
    demand_filtered = demand.loc[:, demand.columns.isin(countries["id"].unique())]
    demand_filtered = demand.loc[:, demand.columns == "ALB"]

    # filter demand
    start = snakemake.config["temporal_scope"]["start"]
    end = snakemake.config["temporal_scope"]["end"]
    demand_filtered = demand_filtered.loc[start:end]

    demand_raster = gregor.timeseries.disaggregate_timeseries_polygon_to_raster(
        demand_filtered, countries, column="demand", proxy=population
    )

    demand_raster.to_netcdf(path_output_data)

    plot_profiles(demand_raster)
    plt.savefig(path_output_plot)

    plot_map(countries, demand_raster)
    plt.savefig(path_output_map)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    main(
        snakemake.input.demand,
        snakemake.input.population,
        snakemake.input.countries,
        snakemake.output.output_data,
        snakemake.output.output_plot,
        snakemake.output.output_map,
    )
