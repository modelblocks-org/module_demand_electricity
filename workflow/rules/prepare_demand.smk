rule demand_electricity_raster:
    input:
        demand=f"<resources>/automatic/{config['use_load']}.parquet",
        countries="<countries>",
        population="<resources>/automatic/population_clean.tif",
    output:
        output_data="<resources>/automatic/demand_electricity_raster.tif",
        output_profiles="<resources>/automatic/demand_electricity_countries_profiles.parquet",
        plot_raster="<results>/demand_electricity_raster_map.png",
        plot_missing="<results>/raw_load_entsoe_missing.png",
        plot_profiles="<results>/raw_load_entsoe_profiles.png",
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
        output_data="<output_data>",
        output_map="<output_map>",
    log:
        "<logs>/demand_electricity_polygon_{name_shapes}.log",
    conda:
        "../envs/gregor.yaml"
    message:
        "Aggregate annual demand to shapes and scale with profile."
    script:
        "../scripts/demand_electricity_polygon.py"
