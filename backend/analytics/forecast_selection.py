
import pandas as pd


def select_forecasts_as_of(
    forecasts: pd.DataFrame,
    cutoff: pd.Timestamp,
) -> pd.DataFrame:
    """Select the latest forecast published before a decision cutoff."""

    if forecasts.empty:
        return forecasts.copy()

    eligible = forecasts[
        forecasts["publish_time"] <= cutoff
    ].copy()

    if eligible.empty:
        return eligible

    selected = (
        eligible
        .sort_values("publish_time")
        .drop_duplicates(
            subset=["delivery_time"],
            keep="last",
        )
        .sort_values("delivery_time")
        .reset_index(drop=True)
    )

    return selected

