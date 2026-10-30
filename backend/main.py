
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import date
from services.elexon import fetch_wind_actuals
from services.elexon import fetch_wind_forecasts


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