"""Prepare electricity demand timeseries, aggregated to shapes."""

import logging

import geopandas as gpd
import gregor
import matplotlib.pyplot as plt
import pandas as pd
import rioxarray as rxr
from _plots import map_polygon
from _schemas import Shapes


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
    path_output_map,
):
    """Aggregate raster demand to polygons and apply profile of the respective country."""
    # load data
    demand_raster = rxr.open_rasterio(path_demand_raster)
    demand_profiles = pd.read_parquet(path_demand_profiles)
    shapes = gpd.read_parquet(path_shapes)
    shapes = Shapes.validate(shapes)

    # use only shapes of class land
    maritime_shapes = shapes.loc[shapes["shape_class"] == "maritime"]
    if not maritime_shapes.empty:
        logger.warning(
            f"Dropping maritime shapes: {maritime_shapes['shape_id'].tolist()}"
        )
    shapes = shapes.loc[shapes["shape_class"] == "land"]
    shapes = shapes[["shape_id", "country_id", "geometry"]].set_index("shape_id")

    # aggregate raster to target shapes
    demand_polygon = gregor.aggregate.aggregate_raster_to_polygon(
        demand_raster.sel(
            band=1
        ),  # TODO: Check why the band dim is introduced when disaggregating
        shapes.geometry,
    )

    # apply profiles
    demand_polygon_profiles = apply_profiles(
        demand_polygon["sum"], shapes, demand_profiles
    )

    # save results and plots
    demand_polygon_profiles.to_parquet(path_output_data)

    map_polygon(demand_polygon)
    plt.savefig(path_output_map)


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    main(
        path_demand_raster=snakemake.input.demand_raster,
        path_demand_profiles=snakemake.input.demand_profiles,
        path_shapes=snakemake.input.shapes,
        path_output_data=snakemake.output.output_data,
        path_output_map=snakemake.output.output_map,
    )
