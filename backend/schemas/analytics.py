
from pydantic import BaseModel


class MetricsResponse(BaseModel):
    mae: float | None
    rmse: float | None
    mape: float | None
    records_count: int


class AnalyticsSummary(BaseModel):
    start_date: str
    end_date: str
    actual_records: int
    forecast_records: int
    metrics: MetricsResponse

