
import pandas as pd


def prepare_actuals(records: list[dict]) -> pd.DataFrame:
    """Convert half-hourly actual generation records into hourly data."""
    df = pd.DataFrame(records)

    if df.empty:
        return pd.DataFrame(columns=["delivery_time", "actual_generation"])

    df["startTime"] = pd.to_datetime(df["startTime"], utc=True)
    df["generation"] = pd.to_numeric(df["generation"], errors="coerce")

    df = df.dropna(subset=["startTime", "generation"])

    # Two half-hourly values are averaged into one hourly value.
    df["delivery_time"] = df["startTime"].dt.floor("h")

    hourly = (
        df.groupby("delivery_time", as_index=False)["generation"]
        .mean()
        .rename(columns={"generation": "actual_generation"})
    )

    return hourly


def prepare_forecasts(records: list[dict]) -> pd.DataFrame:
    """Convert forecast records into a standard DataFrame."""
    df = pd.DataFrame(records)

    if df.empty:
        return pd.DataFrame(
            columns=["delivery_time", "publish_time", "forecast_generation"]
        )

    df["startTime"] = pd.to_datetime(df["startTime"], utc=True)
    df["publishTime"] = pd.to_datetime(df["publishTime"], utc=True)
    df["generation"] = pd.to_numeric(df["generation"], errors="coerce")

    df = df.dropna(
        subset=["startTime", "publishTime", "generation"]
    )

    return df.rename(
        columns={
            "startTime": "delivery_time",
            "publishTime": "publish_time",
            "generation": "forecast_generation",
        }
    )[
        ["delivery_time", "publish_time", "forecast_generation"]
    ]
