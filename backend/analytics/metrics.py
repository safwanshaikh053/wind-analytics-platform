
import pandas as pd


def calculate_metrics(
    actuals: pd.DataFrame,
    forecasts: pd.DataFrame,
) -> dict:
    """Calculate forecast accuracy metrics."""

    if actuals.empty or forecasts.empty:
        return {
            "mae": None,
            "rmse": None,
            "mape": None,
            "records_count": 0,
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

    return {
        "mae": round(float(mae), 2),
        "rmse": round(float(rmse), 2),
        "mape": round(float(mape), 2) if mape is not None else None,
        "records_count": len(merged),
    }
