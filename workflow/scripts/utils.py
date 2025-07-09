"""A collection of small functions shared across scripts."""

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import ListedColormap


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
