from datetime import date
from datetime import date, datetime

import pandas as pd
from fastapi import HTTPException
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.analytics_service import get_wind_analytics
from schemas.analytics import AnalyticsSummary, MetricsResponse
from services.elexon import (
    fetch_wind_actuals,
    fetch_wind_forecasts,
)

app = FastAPI(
    title="Wind Forecast Analytics API",
    description="API for UK wind generation forecasts and forecast accuracy analysis.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Wind Forecast Analytics API is running",
        "status": "ok",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}



@app.get("/api/test-elexon")
async def test_elexon():
    data = await fetch_wind_actuals(
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 2),
    )

    return {
        "records_count": len(data),
        "first_record": data[0] if data else None,
        "last_record": data[-1] if data else None,
    }

@app.get("/api/test-forecast")
async def test_forecast():
    data = await fetch_wind_forecasts(
        start_date=date(2026, 1, 1),
        end_date=date(2026, 1, 2),
    )

    return {
        "records_count": len(data),
        "sample": data[:3],
    }


@app.get("/api/analytics", response_model=AnalyticsSummary)
async def analytics(
    start_date: date,
    end_date: date,
    cutoff: datetime,
):
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date must be before or equal to end_date",
        )

    if cutoff.tzinfo is None or cutoff.utcoffset() is None:
        raise HTTPException(
            status_code=400,
            detail="cutoff must include a timezone, preferably UTC",
        )

    result = await get_wind_analytics(
        start_date=start_date,
        end_date=end_date,
        cutoff=pd.Timestamp(cutoff).tz_convert("UTC"),
    )

    return result