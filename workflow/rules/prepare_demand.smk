rule demand_electricity_raster:
    input:
        demand=f"<resources>/automatic/{config['use_load']}.parquet",
        countries="<countries>",
        population="<resources>/automatic/population_clean.tif",
    output:
        output_data="<resources>/automatic/demand_electricity_raster.tif",
        output_profiles="<resources>/automatic/demand_electricity_countries_profiles.parquet",
        output_map="<resources>/automatic/demand_electricity_raster_map.png",
    log:
        "<logs>/demand_electricity_raster.log",
    conda:
        "../envs/gregor.yaml"
    message:
        "Disaggregate annual demand to raster."
    script:
        "../scripts/demand_electricity_raster.py"


rule demand_electricity_polygon:
    input:
        demand_raster="<resources>/automatic/demand_electricity_raster.tif",
        demand_profiles="<resources>/automatic/demand_electricity_countries_profiles.parquet",
        shapes="<resources>/user/shapes_{name_shapes}.parquet",
    output:
        output_data="results/demand_electricity_{name_shapes}_MW.parquet",
        output_map="results/demand_electricity_{name_shapes}_map.png",
    log:
        "<logs>/demand_electricity_polygon_{name_shapes}.log",
    conda:
        "../envs/gregor.yaml"
    message:
        "Aggregate annual demand to shapes and scale with profile."
    script:
        "../scripts/demand_electricity_polygon.py"
