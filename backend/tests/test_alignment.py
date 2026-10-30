
import pandas as pd

from analytics.alignment import prepare_actuals, prepare_forecasts


def test_prepare_actuals_averages_half_hourly_records():
    records = [
        {
            "startTime": "2026-01-01T00:00:00Z",
            "generation": 100,
        },
        {
            "startTime": "2026-01-01T00:30:00Z",
            "generation": 200,
        },
    ]

    result = prepare_actuals(records)

    assert len(result) == 1
    assert result.iloc[0]["actual_generation"] == 150


def test_prepare_forecasts_preserves_publication_time():
    records = [
        {
            "startTime": "2026-01-01T01:00:00Z",
            "publishTime": "2026-01-01T00:30:00Z",
            "generation": 500,
        }
    ]

    result = prepare_forecasts(records)

    assert len(result) == 1
    assert result.iloc[0]["forecast_generation"] == 500
    assert pd.notna(result.iloc[0]["publish_time"])


def test_prepare_actuals_handles_empty_data():
    result = prepare_actuals([])

    assert result.empty
    assert "actual_generation" in result.columns
