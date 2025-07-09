"""Prepare electricity demand timeseries, aggregated to shapes."""

import logging

import geopandas as gpd
import gregor
import matplotlib.pyplot as plt
import pandas as pd
import rioxarray as rxr

MW_to_GW = 1e-3
GW_to_TW = 1e-3
MW_to_TW = 1e-6


def plot_profiles(profiles):
    """Plot electricity demand profiles."""
    column = profiles.columns[0]
    profiles_example = profiles[column]
    profiles_example = profiles_example * MW_to_GW
    annual_demand = profiles_example.sum() * GW_to_TW

    fig, ax = plt.subplots(figsize=(7, 3))
    profiles_example.plot(
        ax=ax,
        title=f"Annual electricity demand {column}: {annual_demand:.2f} TWh",
        ylabel="Electricity demand [GW]",
        xlabel="Time [h]",
    )

    return fig


def plot_map(demand):
    """Plot annual electricity demand on a map."""
    summed_demand = demand["sum"].sum() * MW_to_TW

    fig, ax = plt.subplots(figsize=(5, 5))
    demand.plot(column="sum", cmap="Reds", legend=True, ax=ax)
    ax.set_title(f"Total annual electricity demand: {summed_demand:.0f} TWh")

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
    # drop regions whose country_id does not correspond to a demand_profile
    country_id_of_region = shapes["country_id"]
    covered_countries = demand_profiles.columns

    countries_not_covered = set(country_id_of_region.unique()).difference(
        covered_countries
    )
    regions_not_covered = country_id_of_region[
        country_id_of_region.isin(countries_not_covered)
    ].index.tolist()

    demand_polygon_covered = demand_polygon.loc[
        ~demand_polygon.index.isin(regions_not_covered)
    ]
    logger.warning(
        f"Regions {regions_not_covered} are not covered by any demand profile and have been dropped."
    )

    # assign profiles to regions
    demand_profiles_mapped = pd.DataFrame(
        {
            region: demand_profiles[country_id_of_region[region]]
            for region in demand_polygon_covered.index
        }
    )

    # multiply with regional annual demand and normalize profiles
    profiles_region = demand_polygon_covered[demand_profiles_mapped.columns].mul(
        demand_profiles_mapped
    )

    # normalize profiles
    profiles_sum = demand_profiles_mapped.sum(axis=0)
    profiles_region = profiles_region.div(profiles_sum, axis="columns")
    profiles_region.columns.name = demand_polygon_covered.index.name

    # check if the sum of the profiles matches the annual demand
    pd.testing.assert_frame_equal(
        profiles_region.sum(axis=0).to_frame(name="sum"),
        demand_polygon_covered.to_frame(name="sum"),
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
    shapes = gpd.read_parquet(path_shapes)[["country_id", "geometry"]]

    demand_polygon = gregor.aggregate.aggregate_raster_to_polygon(
        demand_raster.sel(
            band=1
        ),  # TODO: Check why the band dim is introduced when disaggregating
        shapes.geometry,
    )

    demand_polygon_profiles = apply_profiles(
        demand_polygon["sum"], shapes, demand_profiles
    )

    demand_polygon_profiles.to_parquet(path_output_data)

    plot_profiles(demand_polygon_profiles)
    plt.savefig(path_output_plot)

    plot_map(demand_polygon)
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
