"""A collection of plotting functions shared across scripts."""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import ListedColormap

MW_to_GW = 1e-3
GW_to_TW = 1e-3
MW_to_TW = 1e-6


def plot_missing_values_heatmap(df: pd.DataFrame):
    """Plot a heatmap of missing values."""
    cmap = ListedColormap(["#ffffff", "#E70F0F"], name="binary")

    plt.figure(figsize=(12, 6))
    plt.imshow(df.isna(), aspect="auto", cmap=cmap, interpolation="nearest")
    plt.legend(
        handles=[
            plt.Line2D([0], [0], color="#E70F0F", lw=4, label="Missing"),
            plt.Line2D([0], [0], color="#ffffff", lw=4, label="Present"),
        ],
        bbox_to_anchor=(1.05, 1),
        loc="upper right",
        title="Legend",
        fontsize=10,
        frameon=False,
    )
    plt.title("Missing Values Heatmap for Load Data")
    plt.ylabel("Time Index")
    plt.xlabel("Countries")
    plt.xticks(ticks=range(len(df.columns)), labels=df.columns, rotation=90)

    # Set y-ticks to show every year
    plt.yticks(ticks=range(0, len(df), 8760), labels=df.index[::8760].year, rotation=0)


def plot_profiles(profiles):
    """Plot electricity demand profiles."""
    column = profiles.columns[0]
    profiles_example = profiles[column]
    profiles_example = profiles_example * MW_to_GW
    annual_demand = profiles_example.sum() * GW_to_TW

    fig, ax = plt.subplots(figsize=(7, 3))
    profiles_example.plot(
        ax=ax,
        title=f"Annual electricity demand {column}: {annual_demand:.2f} TWh",
        ylabel="Electricity demand [GW]",
        xlabel="Time [h]",
    )

    return fig


def map_raster(shapes, demand):
    """Plot annual electricity demand on a map."""
    fig, ax = plt.subplots(figsize=(6, 6), dpi=300)

    (
        demand.to_dataarray()
        .coarsen(x=5, y=5, boundary="trim")
        .sum()
        .plot(ax=ax, cmap="magma", vmin=0, vmax=10000, aspect=None)
    )
    shapes.boundary.plot(ax=ax, color="white", alpha=0.3, linewidth=0.5, aspect=None)

    return fig


def map_polygon(demand):
    """Plot annual electricity demand on a map."""
    summed_demand = demand["sum"].sum() * MW_to_TW

    fig, ax = plt.subplots(figsize=(5, 5))
    demand.plot(column="sum", cmap="Reds", legend=True, ax=ax)
    ax.set_title(f"Total annual electricity demand: {summed_demand:.0f} TWh")

    return fig
