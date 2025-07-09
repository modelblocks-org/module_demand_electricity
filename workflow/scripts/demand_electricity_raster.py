"""Prepare electricity demand timeseries at raster resolution."""

import logging

import geopandas as gpd
import gregor
import matplotlib.pyplot as plt
import pandas as pd
import rioxarray as rxr


def plot_map(shapes, demand):
    """Plot annual electricity demand on a map."""
    fig, ax = plt.subplots(figsize=(10, 10))
    demand = demand.to_dataarray().sel(band=1)
    print(demand)

    demand.plot.imshow(cmap="viridis", vmin=0, vmax=19)
    return fig


def main(
    path_demand,
    path_population,
    path_countries,
    path_output_data,
    path_output_profiles,
    path_output_map,
):
    """Main function."""
    demand = pd.read_parquet(path_demand)
    countries = gpd.read_parquet(path_countries).set_index("shape_id")
    population = rxr.open_rasterio(path_population)
    population = population.sel(band=1)

    # match load data with countries
    regions = demand.columns
    missing_countries = set(regions).difference(countries.index.unique())
    logger.info("Drop timeseries for missing countries", missing_countries)
    demand_filtered = demand.loc[:, demand.columns.isin(countries.index.unique())]

    # filter demand
    start = snakemake.config["temporal_scope"]["start"]
    end = snakemake.config["temporal_scope"]["end"]
    demand_filtered = demand_filtered.loc[start:end]

    # drop columns with all zero or all NaN values
    all_nan = demand_filtered.isna().all(axis=0)
    all_zero = (demand_filtered == 0).all(axis=0)
    logger.info(f"Dropping columns with all NaN: {all_nan.loc[all_nan].index.tolist()}")
    logger.info(
        f"Dropping columns with all zero: {all_zero.loc[all_zero].index.tolist()}"
    )
    demand_filtered = demand_filtered.loc[:, ~(all_nan | all_zero)]

    # aggregate demand over time
    demand_sum = demand_filtered.sum(axis=0).to_frame(name="demand")

    # join with countries' geometry
    demand_sum = demand_sum.join(countries["geometry"])
    demand_sum = gpd.GeoDataFrame(demand_sum, geometry="geometry")

    # disaggregate annual demand to raster resolution
    demand_raster = gregor.disaggregate.disaggregate_polygon_to_raster(
        demand_sum, column="demand", proxy=population
    )
    demand_raster.rio.to_raster(path_output_data)

    demand_filtered.to_parquet(path_output_profiles)

    # plot_map(countries, demand_raster)
    plt.savefig(path_output_map)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    main(
        snakemake.input.demand,
        snakemake.input.population,
        snakemake.input.countries,
        snakemake.output.output_data,
        snakemake.output.output_profiles,
        snakemake.output.output_map,
    )
