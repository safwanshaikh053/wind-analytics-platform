from pydantic import BaseModel


class HourlyDataResponse(BaseModel):
    delivery_time: str
    actual_generation: float
    forecast_generation: float
    error: float
    absolute_error: float


class MetricsResponse(BaseModel):
    mae: float | None
    rmse: float | None
    mape: float | None
    records_count: int
    hourly_data: list[HourlyDataResponse]


class AnalyticsSummary(BaseModel):
    start_date: str
    end_date: str
    actual_records: int
    forecast_records: int
    selected_forecasts: int
    metrics: MetricsResponse