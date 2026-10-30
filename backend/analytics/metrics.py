import pandas as pd


def calculate_metrics(
    actuals: pd.DataFrame,
    forecasts: pd.DataFrame,
) -> dict:
    """Calculate forecast accuracy metrics and hourly comparison data."""

    if actuals.empty or forecasts.empty:
        return {
            "mae": None,
            "rmse": None,
            "mape": None,
            "records_count": 0,
            "hourly_data": [],
        }

    merged = pd.merge(
        actuals,
        forecasts,
        on="delivery_time",
        how="inner",
    )

    if merged.empty:
        return {
            "mae": None,
            "rmse": None,
            "mape": None,
            "records_count": 0,
            "hourly_data": [],
        }

    errors = (
        merged["forecast_generation"]
        - merged["actual_generation"]
    )

    absolute_errors = errors.abs()

    mae = absolute_errors.mean()
    rmse = (errors.pow(2).mean()) ** 0.5

    valid_actuals = merged["actual_generation"] != 0

    mape = None

    if valid_actuals.any():
        mape = (
            absolute_errors[valid_actuals]
            / merged.loc[valid_actuals, "actual_generation"].abs()
        ).mean() * 100

    hourly_data = merged.copy()
    hourly_data["error"] = errors
    hourly_data["absolute_error"] = absolute_errors

    hourly_data = hourly_data.sort_values("delivery_time")

    return {
        "mae": round(float(mae), 2),
        "rmse": round(float(rmse), 2),
        "mape": round(float(mape), 2) if mape is not None else None,
        "records_count": len(merged),
        "hourly_data": [
            {
                "delivery_time": row["delivery_time"].isoformat(),
                "actual_generation": round(float(row["actual_generation"]), 2),
                "forecast_generation": round(float(row["forecast_generation"]), 2),
                "error": round(float(row["error"]), 2),
                "absolute_error": round(float(row["absolute_error"]), 2),
            }
            for _, row in hourly_data.iterrows()
        ],
    }