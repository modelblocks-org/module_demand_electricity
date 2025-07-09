rule demand_electricity_raster:
    message:
        "Disaggregate annual demand to raster."
    input:
        demand=f"resources/automatic/{internal['use_load']}.parquet",
        countries="resources/user/countries.parquet",
        population="resources/automatic/population_clean.tif",
    output:
        output_data="resources/automatic/demand_electricity_raster.tif",
        output_profiles="resources/automatic/demand_electricity_countries_profiles.parquet",
        output_map="resources/automatic/demand_electricity_raster_map.png",
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
        demand_raster="resources/automatic/demand_electricity_raster.tif",
        demand_profiles="resources/automatic/demand_electricity_countries_profiles.parquet",
        shapes="resources/user/shapes_{name_shapes}.parquet",
    output:
        output_data="results/demand_electricity_{name_shapes}_profiles.parquet",
        output_plot="results/demand_electricity_{name_shapes}_profiles.png",
        output_map="results/demand_electricity_{name_shapes}_map.png",
    log:
        "logs/demand_electricity_{name_shapes}.log",
    conda:
        "../envs/gregor.yaml"
    script:
        "../scripts/demand_electricity_polygon.py"
