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
        like_vector="<shapes>",
        raster=rules.unzip_population.output[0],
    output:
        path="<resources>/automatic/{shape}/population_clean.tif",
    log:
        "<logs>/{shape}/clean_population.log",
    params:
        buffer=internal["population"]["buffer"],
    wrapper:
        "v9.5.0/geo/rasterio/clip"
