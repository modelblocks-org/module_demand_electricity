rule clean_load_entsoe_opsd:
    input:
        load="<resources>/automatic/load_entsoe_opsd.csv",
    output:
        load="<resources>/automatic/load_entsoe_opsd.parquet",
    log:
        "<logs>/clean_load_entsoe_opsd.log",
    conda:
        "../envs/gregor.yaml"
    script:
        "../scripts/clean_load_entsoe_opsd.py"


rule clean_population:
    input:
        "<resources>/automatic/population_raw.tif",
    output:
        "<resources>/automatic/population_clean.tif",
    log:
        "<logs>/clean_population.log",
    conda:
        "../envs/gregor.yaml"
    params:
        minx=internal["population"]["minx"],
        miny=internal["population"]["miny"],
        maxx=internal["population"]["maxx"],
        maxy=internal["population"]["maxy"],
    script:
        "../scripts/clean_population.py"
