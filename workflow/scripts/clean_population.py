"""Clean population data."""

import sys
from typing import TYPE_CHECKING, Any

import geopandas as gpd
import rioxarray as rxr
from shapely.geometry import box

if TYPE_CHECKING:
    snakemake: Any


def main(path_raw, minx, miny, maxx, maxy, path_clean):
    """Main function."""
    population = rxr.open_rasterio(path_raw)

    # clip to spatial scope
    clipping_box = gpd.GeoDataFrame(
        geometry=[box(minx, miny, maxx, maxy)], crs="EPSG:4326"
    )

    population = population.rio.clip(clipping_box.to_crs(population.rio.crs).geometry)

    population.rio.to_raster(path_clean)


if __name__ == "__main__":
    sys.stderr = open(snakemake.log[0], "w", buffering=1)
    main(
        path_raw=snakemake.input[0],
        minx=snakemake.params.minx,
        miny=snakemake.params.miny,
        maxx=snakemake.params.maxx,
        maxy=snakemake.params.maxy,
        path_clean=snakemake.output[0],
    )
