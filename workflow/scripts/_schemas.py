"""Schemas for key files."""

# ruff: noqa: UP007
from pathlib import Path

import pandas as pd
import yaml
from pandera.pandas import DataFrameModel, Field
from pandera.typing.geopandas import GeoSeries
from pandera.typing.pandas import Series


def read_yaml(path):
    """Read a YAML file."""
    with open(path) as file:
        return yaml.safe_load(file)


path_map_countries_ENTSOE = (
    Path(__file__).parent.parent / "internal" / "map_countries_ENTSOE.yaml"
)
country_codes = read_yaml(path_map_countries_ENTSOE).values()


class LoadENTSOE(DataFrameModel):
    class Config:
        coerce = True
        strict = False

    region: Series[str]  # = Field(isin=[country_codes])
    "2-letter country code."
    variable: Series[str]  #  = Field(isin=["load"])
    "Variable."
    attribute: Series[str] = Field(isin=["actual_entsoe_power_statistics"])
    "Attribute."
    utc_timestamp: Series[pd.Timestamp]
    "UTC timestamp."
    data: Series[float]
    "Load data."


class Shapes(DataFrameModel):
    class Config:
        coerce = True
        strict = False

    shape_id: Series[str]
    "Shape ID."
    country_id: Series[str]
    "Country ID."
    shape_class: Series[str] = Field(isin=["land", "maritime"])
    "Shape class."
    geometry: GeoSeries
    "Geometry."
