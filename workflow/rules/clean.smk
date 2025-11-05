rule clean_load_entsoe_opsd:
    input:
        load="resources/automatic/load_entsoe_opsd.csv",
        map_countries=workflow.source_path("../internal/map_countries_ENTSOE.yaml"),
    output:
        load="resources/automatic/load_entsoe_opsd.parquet",
        plot_missing="resources/automatic/load_entsoe_opsd.png",
        plot_profiles="resources/automatic/load_entsoe_opsd_profiles.png",
    log:
        "logs/clean_load.log",
    conda:
        "../envs/shell.yaml"
    script:
        "../scripts/clean_load_entsoe_opsd.py"


rule clean_population:
    input:
        "resources/automatic/population/GHS_POP_E2020_GLOBE_R2023A_54009_1000_V1_0.tif",
    output:
        "resources/automatic/population_clean.tif",
    params:
        minx=internal["population"]["minx"],
        miny=internal["population"]["miny"],
        maxx=internal["population"]["maxx"],
        maxy=internal["population"]["maxy"],
    log:
        "logs/clean_population.log",
    conda:
        "../envs/shell.yaml"
    script:
        "../scripts/clean_population.py"
