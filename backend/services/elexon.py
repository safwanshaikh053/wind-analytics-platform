
from datetime import date

import httpx

BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1"


async def fetch_wind_actuals(
    start_date: date,
    end_date: date,
) -> list[dict]:
    """Fetch actual wind generation for a date range."""
    url = f"{BASE_URL}/datasets/FUELHH/stream"

    params = {
        "settlementDateFrom": start_date.isoformat(),
        "settlementDateTo": end_date.isoformat(),
        "fuelType": "WIND",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    if isinstance(data, dict):
        data = data.get("data", [])

    return data


async def fetch_wind_forecasts(
    start_date: date,
    end_date: date,
) -> list[dict]:
    """Fetch wind-generation forecasts for a date range."""
    url = f"{BASE_URL}/datasets/WINDFOR/stream"

    params = {
        "publishDateTimeFrom": f"{start_date.isoformat()}T00:00:00Z",
        "publishDateTimeTo": f"{end_date.isoformat()}T23:59:59Z",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()

    if isinstance(data, dict):
        data = data.get("data", [])

    return data
