
import pandas as pd

from analytics.forecast_selection import select_forecasts_as_of


def test_selects_latest_forecast_before_cutoff():
    forecasts = pd.DataFrame({
        "delivery_time": pd.to_datetime([
            "2026-01-02T12:00:00Z",
            "2026-01-02T12:00:00Z",
            "2026-01-02T12:00:00Z",
        ]),
        "publish_time": pd.to_datetime([
            "2026-01-02T06:00:00Z",
            "2026-01-02T09:00:00Z",
            "2026-01-02T11:00:00Z",
        ]),
        "forecast_generation": [1000, 1200, 1500],
    })

    cutoff = pd.Timestamp("2026-01-02T10:00:00Z")

    result = select_forecasts_as_of(forecasts, cutoff)

    assert len(result) == 1
    assert result.iloc[0]["forecast_generation"] == 1200
    assert result.iloc[0]["publish_time"] == pd.Timestamp(
        "2026-01-02T09:00:00Z"
    )


def test_excludes_forecasts_published_after_cutoff():
    forecasts = pd.DataFrame({
        "delivery_time": pd.to_datetime([
            "2026-01-02T12:00:00Z",
        ]),
        "publish_time": pd.to_datetime([
            "2026-01-02T11:00:00Z",
        ]),
        "forecast_generation": [1500],
    })

    cutoff = pd.Timestamp("2026-01-02T10:00:00Z")

    result = select_forecasts_as_of(forecasts, cutoff)

    assert result.empty
