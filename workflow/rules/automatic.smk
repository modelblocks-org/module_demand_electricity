"""Rules to used to download automatic resource files."""


rule download_resources:
    message:
        "Download resources."
    params:
        url_load=internal["resources"]["automatic"]["load"],
        url_population=internal["resources"]["automatic"]["population"],
    output:
        load="resources/automatic/load.csv",
        population="resources/automatic/population.zip",
    log:
        "logs/download_resources.log",
    conda:
        "../envs/shell.yaml"
    shell:
        """
        curl -sSLo {output.load} '{params.url_load}'
        curl -sSLo {output.population} '{params.url_population}'
        """


rule unzip:
    message:
        "Unzip population data."
    input:
        "resources/automatic/population.zip",
    output:
        directory=directory("resources/automatic/population"),
        population_clean="resources/automatic/population/GHS_POP_E2020_GLOBE_R2023A_54009_1000_V1_0.tif",
    log:
        "logs/unzip.log",
    conda:
        "../envs/shell.yaml"
    shell:
        "unzip -o {input} -d {output.directory}"
