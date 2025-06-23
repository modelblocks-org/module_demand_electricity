rule clean_load:
    input:
        "resources/automatic/load.csv",
    output:
        "resources/automatic/load_clean.parquet",
    log:
        "logs/clean_load.log",
    conda:
        "../envs/shell.yaml"
    script:
        "../scripts/clean_load.py"


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
