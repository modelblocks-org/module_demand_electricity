"""Clean population data."""

import geopandas as gpd
import rioxarray as rxr
from shapely.geometry import box


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
    main(
        path_raw=snakemake.input[0],
        minx=snakemake.params.minx,
        miny=snakemake.params.miny,
        maxx=snakemake.params.maxx,
        maxy=snakemake.params.maxy,
        path_clean=snakemake.output[0],
    )
