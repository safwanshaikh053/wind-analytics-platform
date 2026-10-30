
from datetime import date

import pandas as pd

from analytics.alignment import (
    prepare_actuals,
    prepare_forecasts,
)
from analytics.forecast_selection import select_forecasts_as_of
from analytics.metrics import calculate_metrics
from services.elexon import (
    fetch_wind_actuals,
    fetch_wind_forecasts,
)


async def get_wind_analytics(
    start_date: date,
    end_date: date,
    cutoff: pd.Timestamp,
) -> dict:
    """Fetch, process and analyse wind generation data."""

    actual_records = await fetch_wind_actuals(
        start_date,
        end_date,
    )

    forecast_records = await fetch_wind_forecasts(
        start_date,
        end_date,
    )

    actuals = prepare_actuals(actual_records)
    forecasts = prepare_forecasts(forecast_records)

    selected_forecasts = select_forecasts_as_of(
        forecasts,
        cutoff,
    )

    metrics = calculate_metrics(
        actuals,
        selected_forecasts,
    )

    return {
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "actual_records": len(actual_records),
        "forecast_records": len(forecast_records),
        "selected_forecasts": len(selected_forecasts),
        "metrics": metrics,
    }
