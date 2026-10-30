import pandas as pd

from analytics.forecast_selection import select_forecasts_as_of


def test_selects_latest_forecast_before_day_ahead_cutoff():
    forecasts = pd.DataFrame({
        "delivery_time": pd.to_datetime([
            "2026-01-02T12:00:00Z",
            "2026-01-02T12:00:00Z",
            "2026-01-02T12:00:00Z",
            "2026-01-02T12:00:00Z",
        ]),
        "publish_time": pd.to_datetime([
            "2026-01-01T06:00:00Z",
            "2026-01-01T09:00:00Z",
            "2026-01-01T11:00:00Z",
            "2026-01-01T11:30:00Z",
        ]),
        "forecast_generation": [1000, 1200, 1500, 1800],
    })

    result = select_forecasts_as_of(forecasts)

    assert len(result) == 1
    assert result.iloc[0]["forecast_generation"] == 1500
    assert result.iloc[0]["publish_time"] == pd.Timestamp(
        "2026-01-01T11:00:00Z"
    )


def test_excludes_forecasts_published_after_day_ahead_cutoff():
    forecasts = pd.DataFrame({
        "delivery_time": pd.to_datetime([
            "2026-01-02T12:00:00Z",
        ]),
        "publish_time": pd.to_datetime([
            "2026-01-01T11:30:00Z",
        ]),
        "forecast_generation": [1500],
    })

    result = select_forecasts_as_of(forecasts)

    assert result.empty


def test_uses_separate_cutoff_for_each_delivery_date():
    forecasts = pd.DataFrame({
        "delivery_time": pd.to_datetime([
            "2026-01-02T12:00:00Z",
            "2026-01-03T12:00:00Z",
        ]),
        "publish_time": pd.to_datetime([
            "2026-01-01T10:00:00Z",
            "2026-01-02T10:00:00Z",
        ]),
        "forecast_generation": [1500, 2000],
    })

    result = select_forecasts_as_of(forecasts)

    assert len(result) == 2
    assert result["forecast_generation"].tolist() == [1500, 2000]