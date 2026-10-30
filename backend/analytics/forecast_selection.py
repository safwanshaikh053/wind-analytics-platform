import pandas as pd


def select_forecasts_as_of(forecasts: pd.DataFrame) -> pd.DataFrame:
    """
    Select the latest forecast published by 11:00 UTC
    on the day before each delivery date.
    """

    if forecasts.empty:
        return forecasts.copy()

    df = forecasts.copy()

    # Calculate the day-ahead cutoff for each delivery date.
    df["cutoff_time"] = (
        df["delivery_time"].dt.normalize()
        - pd.Timedelta(days=1)
        + pd.Timedelta(hours=11)
    )

    # Exclude forecasts published after the cutoff.
    eligible = df[df["publish_time"] <= df["cutoff_time"]].copy()

    if eligible.empty:
        return eligible

    # Select the latest eligible forecast for each delivery hour.
    selected = (
        eligible.sort_values("publish_time")
        .drop_duplicates(subset=["delivery_time"], keep="last")
        .sort_values("delivery_time")
        .reset_index(drop=True)
    )

    return selected.drop(columns=["cutoff_time"])