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


rule clean_population_remote:
    input:
        raster=rules.unzip_population.output[0],
    output:
        path="<resources>/automatic/population_clean.tif",
    params:
        bounds=internal["population"]["bounds"],
        bounds_crs=internal["population"]["crs"],
        buffer=internal["population"]["buffer"]
    log:
        "<logs>/clean_population.log",
    wrapper:
        "v9.5.0/geo/rasterio/clip"
