"""Group 4 (w01) - segments: splits the shop's customers into k segments with k-means on recency, orders and revenue.

Authors: Mateusz, Kacper, Władysław
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from ml_base import Analysis

FEATURES = ["recency_days", "orders", "revenue"]


class CustomerSegments(Analysis):
    """Puts every customer into one of k segments (k-means on recency_days, orders and revenue).

    Usage:
        seg = CustomerSegments(customers, k=4, scale=True).fit()
        seg.results_        # Series: segment number (0..k-1) per CustomerID
        seg.profile()       # one row per segment: size, means, % who came back
        seg.plot()          # orders vs revenue (log-log), coloured by segment

    Args:
        customers: DataFrame with the columns recency_days, orders, revenue (index = CustomerID).
            A `returned` column (0/1) is optional; with it, profile() also shows returned_pct.
        k: number of segments, an integer >= 2.
        scale: True = log1p + StandardScaler before k-means (recommended),
            False = k-means on the raw numbers (revenue in GBP then dominates every distance).

    Raises:
        TypeError: customers is not a DataFrame, or k is not an integer, or scale is not a bool
        ValueError: a required column is missing, k < 2, k > number of customers,
            or the three columns contain missing or negative values
    """
    required_columns = FEATURES

    def __init__(self, customers, k=4, scale=True):
        super().__init__(customers)
        if isinstance(k, bool) or not isinstance(k, (int, np.integer)):
            raise TypeError(f"k must be an integer, got {k!r}")
        if k < 2:
            raise ValueError(f"k must be at least 2, got {k}")
        if k > len(self.data):
            raise ValueError(f"k = {k} is more than the {len(self.data)} customers in the table")
        if not isinstance(scale, (bool, np.bool_)):
            raise TypeError(f"scale must be True or False, got {scale!r}")
        values = self.data[FEATURES]
        if values.isna().any().any():
            raise ValueError("recency_days, orders and revenue must not contain missing values")
        if (values < 0).any().any():
            raise ValueError("recency_days, orders and revenue must not be negative")
        self.k = int(k)
        self.scale = bool(scale)

    def _matrix(self):
        """The numbers k-means sees: log1p + StandardScaler if scale=True, else the raw columns."""
        X = self.data[FEATURES].to_numpy(dtype=float)
        if self.scale:
            X = StandardScaler().fit_transform(np.log1p(X))
        return X

    def fit(self):
        """Runs KMeans(n_clusters=k, n_init=10, random_state=0) on the 3 columns.

        Stores a Series of segment numbers (0..k-1, index = CustomerID, name "segment")
        in self.results_ and returns self.
        """
        model = KMeans(n_clusters=self.k, n_init=10, random_state=0).fit(self._matrix())
        self.model_ = model
        self.results_ = pd.Series(model.labels_, index=self.data.index, name="segment")
        return self

    def profile(self):
        """One row per segment, sorted by mean revenue (highest first).

        Returns:
            DataFrame indexed by segment number with the columns
            customers (how many), recency_days, orders, revenue (means, 1 decimal)
            and returned_pct (% of the segment who bought again Sep-Dec 2011, 1 decimal;
            only if the table has a `returned` column).

        Raises:
            RuntimeError: if fit() was not called
        """
        self.check_fitted()
        groups = self.data.groupby(self.results_)
        table = groups[FEATURES].mean()
        table.insert(0, "customers", groups.size())
        if "returned" in self.data.columns:
            table["returned_pct"] = groups["returned"].mean() * 100
        table.index.name = "segment"
        return table.sort_values("revenue", ascending=False).round(1)

    def plot(self, ax=None):
        """Scatter of orders (x) vs revenue (y), both on a log scale, coloured by segment.

        Args:
            ax: optional matplotlib Axes to draw on (a new figure is made if None).

        Returns:
            the matplotlib Axes

        Raises:
            RuntimeError: if fit() was not called
        """
        self.check_fitted()
        if ax is None:
            _, ax = plt.subplots(figsize=(7, 5))
        cmap = plt.get_cmap("tab10")
        for seg in sorted(self.results_.unique()):
            rows = self.results_ == seg
            ax.scatter(self.data.loc[rows, "orders"], self.data.loc[rows, "revenue"],
                       s=10, alpha=0.6, color=cmap(seg % 10), label=f"segment {seg}")
        ax.set(xscale="log", yscale="log", xlabel="orders (log scale)", ylabel="revenue, GBP (log scale)",
               title=f"{self.k} customer segments ({'scaled' if self.scale else 'raw numbers'})")
        ax.legend(markerscale=2, fontsize=8)
        return ax
