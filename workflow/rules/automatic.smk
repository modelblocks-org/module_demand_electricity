"""Rules to used to download automatic resource files."""


rule download_load_entsoe_api:
    input:
        token_entsoe="<resources>/user/token_entsoe.txt",
    output:
        load="<resources>/automatic/load_entsoe_api.parquet",
        plot_missing="<resources>/automatic/load_entsoe_api_missing.png",
        plot_profiles="<resources>/automatic/load_entsoe_api_profiles.png",
    log:
        "<logs>/download_load_entsoe_api.log",
    conda:
        "../envs/gregor.yaml"
    params:
        country_codes_entsoe=internal["load_entsoe_api"]["countries"],
    message:
        "Download electricity load from ENTSOE."
    script:
        "../scripts/download_load_entsoe_api.py"


rule download_load_entsoe_opsd:
    output:
        load="<resources>/automatic/load_entsoe_opsd.csv",
    log:
        "<logs>/download_load_entsoe_opsd.log",
    conda:
        "../envs/shell.yaml"
    params:
        url_load=internal["resources"]["automatic"]["load_entsoe_opsd"],
    message:
        "Download load profiles from Open Power System Data (OPSD)."
    shell:
        """
        curl -sSLo {output.load} '{params.url_load}'
        """


rule download_population:
    output:
        population="<resources>/automatic/population.zip",
    log:
        "<logs>/download_population.log",
    conda:
        "../envs/shell.yaml"
    params:
        url_population=internal["resources"]["automatic"]["population"],
    message:
        "Download population data."
    shell:
        """
        curl -sSLo {output.population} '{params.url_population}'
        """


rule unzip:
    input:
        "<resources>/automatic/population.zip",
    output:
        directory=directory("<resources>/automatic/population"),
        population_clean="<resources>/automatic/population/GHS_POP_E2020_GLOBE_R2023A_54009_1000_V1_0.tif",
    log:
        "<logs>/unzip.log",
    conda:
        "../envs/shell.yaml"
    message:
        "Unzip population data."
    shell:
        "unzip -o {input} -d {output.directory}"
