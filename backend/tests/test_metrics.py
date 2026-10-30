
import pandas as pd

from analytics.metrics import calculate_metrics


def test_calculate_metrics():
    actuals = pd.DataFrame({
        "delivery_time": pd.to_datetime([
            "2026-01-01T00:00:00Z",
            "2026-01-01T01:00:00Z",
        ]),
        "actual_generation": [100, 200],
    })

    forecasts = pd.DataFrame({
        "delivery_time": pd.to_datetime([
            "2026-01-01T00:00:00Z",
            "2026-01-01T01:00:00Z",
        ]),
        "forecast_generation": [110, 180],
    })

    result = calculate_metrics(actuals, forecasts)

    assert result["mae"] == 15
    assert result["rmse"] == 15.81
    assert result["mape"] == 10
    assert result["records_count"] == 2


def test_calculate_metrics_with_empty_data():
    actuals = pd.DataFrame()
    forecasts = pd.DataFrame()

    result = calculate_metrics(actuals, forecasts)

    assert result["mae"] is None
    assert result["rmse"] is None
    assert result["mape"] is None
    assert result["records_count"] == 0

