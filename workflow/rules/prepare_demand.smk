rule demand_electricity_raster:
    message:
        "Disaggregate demand profiles to raster."
    input:
        demand="resources/automatic/load_clean.parquet",
        countries="resources/user/countries.geojson",
        population="resources/automatic/population_clean.tif",
    output:
        output_data="results/demand_electricity.nc",
        output_plot="results/demand_electricity.png",
        output_map="results/demand_electricity_map.png",
    log:
        "logs/demand_electricity_raster.log",
    conda:
        "../envs/gregor.yaml"
    script:
        "../scripts/demand_electricity_raster.py"
