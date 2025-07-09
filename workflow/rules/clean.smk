rule clean_load_entsoe_opsd:
    input:
        load="resources/automatic/load_entsoe_opsd.csv",
        map_countries=workflow.source_path("../internal/map_countries_ENTSOE.yaml"),
    output:
        load="resources/automatic/load_entsoe_opsd.parquet",
        plot="resources/automatic/load_entsoe_opsd.png",
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
    log:
        "logs/clean_population.log",
    conda:
        "../envs/shell.yaml"
    script:
        "../scripts/clean_population.py"
