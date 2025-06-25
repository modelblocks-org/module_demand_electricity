"""Prepare electricity demand timeseries, aggregated to shapes."""

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


def apply_profiles(demand_polygon, shapes, demand_profiles):
    """Apply profiles to produce demand profiles for regions.

    Produce demand profiles for each region by applying the countries' demand
    profiles to the aggregated annual demand of the regions.

    Parameters
    ----------
    demand_polygon : gdp.GeoDataFrame
        Annual demand per region.
    shapes : gpd.GeoDataFrame
        Contains the country_id and geometry of each region.
    demand_profiles : pd.DataFrame
        Contains the demand profiles for each country.

    Returns:
    -------
    pd.DataFrame
        Demand profiles for each region.

    """
    demand_region_annual = demand_polygon["sum"]
    region_in_country = shapes["country_id"]
    covered_countries = demand_profiles.columns

    # limit to covered regions
    regions_not_covered = set(region_in_country.unique()).difference(covered_countries)
    logger.info(f"Regions not covered by profiles: {regions_not_covered}")
    region_in_country_covered = region_in_country.loc[
        region_in_country.isin(covered_countries)
    ]
    demand_region_annual_covered = demand_region_annual.loc[
        demand_region_annual.index.isin(region_in_country_covered.index)
    ]

    # map profiles to regions
    demand_profiles_mapped = pd.DataFrame(
        {
            region: demand_profiles[region_in_country[region]]
            for region in region_in_country_covered.index
        }
    )

    # multiply with regional annual demand and normalize profiles
    profiles_sum = demand_profiles_mapped.sum(axis=0)
    profiles_region = demand_region_annual_covered[demand_profiles_mapped.columns].mul(
        demand_profiles_mapped
    )
    profiles_region = profiles_region.div(profiles_sum, axis="columns")
    profiles_region.columns.name = demand_region_annual_covered.index.name

    # check if the sum of the profiles matches the annual demand
    pd.testing.assert_frame_equal(
        profiles_region.sum(axis=0, skipna=False).to_frame(name="sum"),
        demand_region_annual_covered.to_frame(name="sum"),
        # rtol=1e-5,
    )
    return profiles_region


def main(
    path_demand_raster,
    path_demand_profiles,
    path_shapes,
    path_output_data,
    path_output_plot,
    path_output_map,
):
    """Main function."""
    demand_raster = rxr.open_rasterio(path_demand_raster)
    demand_profiles = pd.read_parquet(path_demand_profiles)
    shapes = gpd.read_parquet(path_shapes).set_index("shape_id")[
        ["country_id", "geometry"]
    ]

    demand_polygon = gregor.aggregate.aggregate_raster_to_polygon(
        demand_raster.sel(
            band=1
        ),  # TODO: Check why the band dim is introduced when disaggregating
        shapes.geometry,
    )

    demand_polygon_profiles = apply_profiles(demand_polygon, shapes, demand_profiles)

    demand_polygon_profiles.to_parquet(path_output_data)

    plot_profiles(demand_polygon)
    plt.savefig(path_output_plot)

    plot_map(shapes, demand_polygon)
    plt.savefig(path_output_map)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    main(
        snakemake.input.demand_raster,
        snakemake.input.demand_profiles,
        snakemake.input.shapes,
        snakemake.output.output_data,
        snakemake.output.output_plot,
        snakemake.output.output_map,
    )
