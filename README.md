# Data module for electricity demand in Europe

This data module prepares electricity demand timeseries for Europe at arbitrary resolution. The workflow consists of these steps:

- Download ENTSO-E historical load profiles.
- Download a gridded population dataset that serves as a disaggregation proxy.
- Clean the raw data and clip population to ENTSO-E area.
- Disaggregate the national annual load to raster, using population as weight.
- Aggregate the annual load raster data to the target shapes.
- Assign the corresponding national load profile to each region to get the final load profiles for the target shapes.

This is a modular `snakemake` workflow built for [`clio`](https://clio.readthedocs.io/) data modules.

## Using this module

This module can be imported directly into any `snakemake` workflow.
Please consult the integration example in `tests/integration/Snakefile` for more information.

## Development

We use [`pixi`](https://pixi.sh/) as our package manager for development.
Once installed, run the following to clone this repo and install all dependencies.

```shell
git clone git@github.com:calliope-project/module_demand_electricity.git
cd module_demand_electricity
pixi install --all
```

For testing, simply run:

```shell
pixi run test
```

To view the documentation locally, use:

```shell
pixi run serve-docs
```

To test a minimal example of a workflow using this module:

```shell
pixi shell    # activate this project's environment
cd tests/integration/  # navigate to the integration example
snakemake --use-conda  # run the workflow!
```
