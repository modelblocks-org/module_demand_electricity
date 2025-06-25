rule demand_electricity_raster:
    message:
        "Disaggregate annual demand to raster."
    input:
        demand="resources/automatic/load_clean.parquet",
        countries="resources/user/countries.geojson",
        population="resources/automatic/population_clean.tif",
    output:
        output_data="results/demand_electricity_raster.nc",
        output_profiles="results/demand_electricity_countries_profiles.parquet",
        output_map="results/demand_electricity_raster_map.png",
    log:
        "logs/demand_electricity_raster.log",
    conda:
        "../envs/gregor.yaml"
    script:
        "../scripts/demand_electricity_raster.py"


rule demand_electricity_polygon:
    message:
        "Aggregate annual demand to shapes and scale with profile."
    input:
        demand_raster="results/demand_electricity_raster.nc",
        demand_profiles="results/demand_electricity_countries_profiles.parquet",
        shapes="resources/user/shapes.parquet",
    output:
        output_data="results/demand_electricity_polygon_profiles.parquet",
        output_plot="results/demand_electricity_polygon_profiles.png",
        output_map="results/demand_electricity_polygon_map.png",
    log:
        "logs/demand_electricity_polygon.log",
    conda:
        "../envs/gregor.yaml"
    script:
        "../scripts/demand_electricity_polygon.py"
