"""A collection of plotting functions shared across scripts."""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
from matplotlib.dates import DateFormatter

MW_to_GW = 1e-3
GW_to_TW = 1e-3
MW_to_TW = 1e-6


WhiteToRed = LinearSegmentedColormap.from_list("WhiteToRed", ["#ffffff", "#ff0000"])


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


def plot_national_profiles(df: pd.DataFrame):
    """Plot electricity demand profiles for all countries."""
    profiles_GW = df * MW_to_GW
    profiles_GW.loc[:, profiles_GW.isna().all()] = 0
    profiles_GW_d = profiles_GW.resample("1D").mean()

    n_profiles = df.shape[1]

    fig, axs = plt.subplots(1, n_profiles, figsize=(17, 6))
    fig.subplots_adjust(wspace=0)

    for ax, column in zip(axs, profiles_GW.columns):
        ax.plot(
            profiles_GW[column], profiles_GW.index, label=column, color="C0", alpha=0.3
        )
        ax.plot(
            profiles_GW_d[column],
            profiles_GW_d.index,
            label=f"{column} (daily mean)",
            color="k",
            linewidth=1,
        )
        val_max = profiles_GW[column].max()
        val_max = val_max if val_max > 0 else 1
        ax.set_xlim(0, val_max * 1.1)
        ax.set_xticks([0, np.round(val_max, 1)])
        ax.set_xticklabels(["", np.round(val_max, 1)])
        ax.title.set_text(column)

    for ax in axs.flatten()[1:]:
        ax.set_yticks([])

    axs[0].set_ylabel("Time [h]")
    axs[0].yaxis.set_major_formatter(DateFormatter("%Y-%m"))
    axs[0].set_xlabel("Electricity load [GW]")

    fig.suptitle("National electricity load for ENTSO-E countries")

    return fig


def map_raster(shapes, demand):
    """Plot annual electricity demand on a map."""
    fig, ax = plt.subplots(figsize=(7, 6), dpi=300)

    demand_coarse = demand.to_dataarray().coarsen(x=5, y=5, boundary="trim").sum()

    demand_coarse = demand_coarse.rio.write_crs(demand.rio.crs)
    demand_coarse = demand_coarse.rio.write_transform(demand.rio.transform())

    demand_coarse.plot(ax=ax, cmap=WhiteToRed, vmin=0, vmax=10000, aspect=None)

    shapes.boundary.plot(ax=ax, color="white", alpha=0.3, linewidth=0.5, aspect=None)

    return fig


def map_polygon(demand):
    """Plot annual electricity demand on a map."""
    summed_demand = demand["sum"].sum() * MW_to_TW

    fig, ax = plt.subplots(figsize=(7, 6))
    demand.plot(ax=ax, column="sum", cmap=WhiteToRed, legend=True, aspect=None)
    demand.geometry.boundary.plot(
        ax=ax, color="white", alpha=0.3, linewidth=0.5, aspect=None
    )
    demand.geometry.boundary.plot(
        ax=ax, color="k", alpha=0.3, linewidth=0.3, aspect=None
    )

    ax.set_title(f"Total annual electricity demand:\n{summed_demand:.0f} TWh")

    return fig
