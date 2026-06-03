"""
This module is designed to create heatmaps displaying confidence interval overlap (or lack
thereof).
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
# import dec_util


def heatmap(df, color_palette, cmap, title, legend="", path_out=None, show=False, ax=None):
    """
    Creates a heatmap using the given DataFrame, color palette, color map,
    and title.
    """
    # Create figure if needed.
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 10))

    # Heatmap.
    sns.heatmap(
        df,
        linewidths=2,
        square=True,
        cmap=cmap, cbar=False,
        ax=ax
    )
    # Cross-hatching to display information in
    # multiple ways for accessibility.
    range_plot = np.arange(len(df.columns) + 1)
    hatch_logical = np.ma.masked_not_equal(df.values, 10)
    ax.pcolor(
        range_plot, range_plot,
        hatch_logical,
        hatch="//", linewidth=30.0, alpha=0.0
    )
    # Tick marks.
    ax.xaxis.tick_top()
    plt.tick_params(left=False, bottom=False, top=False)
    # tick_labels = [x.replace("Men ", "") for x in dec_util.events]
    tick_labels = [x.replace("X", "").upper() for x in df.index]
    ax.set_xticks(ticks=[i + 0.5 for i in range(10)], labels=tick_labels, fontsize=16, rotation=90)
    ax.set_yticks(ticks=[i + 0.5 for i in range(10)], labels=tick_labels, fontsize=16, rotation=45)
    ax.xaxis.set_label_position('bottom')
    ax.set_xlabel(title, fontsize=24)
    if path_out is not None:
        plt.savefig(path_out)
    if show:
        plt.show()

# Load data.
df_boot_CI = pd.read_csv("output/boot_ci_matrix_gamma.csv", index_col=0)

# Create color palette.
h_neg = 220
h_pos = 20
color_vals = (0.85, 0.4, 0.1)
color_palette = sns.diverging_palette(h_neg, h_pos)
cmap = sns.diverging_palette(h_neg, h_pos, as_cmap=True)

# Define image output path.
path_img_out = "output/images/"

# Heatmaps, boot CIs.
# legend =\
# """
# Figure 1: Matrix diagram showing significant differences between gamma regression coefficients. A hatched orange square indicates that the entirety of the bootstrapped confidence interval of the difference between the row coefficient and column coefficient is below zero, indicating the column coefficient is greater. A teal square indicates that the entire confidence interval is above 0, meaning that the row coefficient is greater. A grey square indicates that this interval contains 0, which means that neither one is significantly greater than the other.
# """
legend = ""

fig, axs = plt.subplots(ncols=1, nrows=1, figsize=(16, 16))
heatmap(df_boot_CI, color_palette=color_palette, cmap=cmap, title="", ax=axs, show=False)
fig.text(0, -0.01, s=legend, fontsize=18, wrap=True)
# plt.tight_layout(h_pad=5.0)
# plt.suptitle("FSB Features", fontsize=24)
plt.savefig(path_img_out + "boot_CI_matrix_gamma.png")

