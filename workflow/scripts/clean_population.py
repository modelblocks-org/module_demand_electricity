"""Clean population data."""

import geopandas as gpd
import numpy as np
import rioxarray as rxr
from shapely.geometry import box


def main(path_raw, path_clean):
    """Main function."""
    population = rxr.open_rasterio(path_raw)

    # clip to spatial scope
    clipping_box = gpd.GeoDataFrame(
        geometry=[
            box(
                snakemake.config["spatial_scope"]["minx"],
                snakemake.config["spatial_scope"]["miny"],
                snakemake.config["spatial_scope"]["maxx"],
                snakemake.config["spatial_scope"]["maxy"],
            )
        ],
        crs="EPSG:4326",
    )
    print(population.rio.crs)
    population = population.rio.clip(clipping_box.to_crs(population.rio.crs).geometry)

    fill_value = population.attrs.get("_FillValue", np.nan)

    # Replace fill value with zero in the data array
    data_filled = population.where(population != fill_value, 0)

    # Update the _FillValue attribute to zero
    data_filled.attrs["_FillValue"] = 0

    data_filled.rio.to_raster(path_clean)


if __name__ == "__main__":
    main(snakemake.input[0], snakemake.output[0])
