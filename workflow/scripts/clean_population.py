"""Clean population data."""

import geopandas as gpd
import numpy as np
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

    fill_value = population.attrs.get("_FillValue", np.nan)

    # Replace fill value with zero in the data array
    data_filled = population.where(population != fill_value, 0)

    # Update the _FillValue attribute to zero
    data_filled.attrs["_FillValue"] = 0

    data_filled.rio.to_raster(path_clean)


if __name__ == "__main__":
    main(
        path_raw=snakemake.input[0],
        minx=snakemake.config["spatial_scope"]["minx"],
        miny=snakemake.config["spatial_scope"]["miny"],
        maxx=snakemake.config["spatial_scope"]["maxx"],
        maxy=snakemake.config["spatial_scope"]["maxy"],
        path_clean=snakemake.output[0],
    )
