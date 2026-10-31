# WindScope – Renewable Energy Intelligence

A renewable energy analytics platform that evaluates day-ahead wind generation forecasts against actual wind generation in Great Britain using official Elexon BMRS data.

**Live Application:** https://wind-analytics-platform.vercel.app/

**Backend API:** https://wind-analytics-backend.onrender.com/

**GitHub Repository:** https://github.com/safwanshaikh053/wind-analytics-platform

---

## 1. Project Overview

WindScope is designed to help energy trading and procurement teams understand the accuracy of wind generation forecasts.

Wind generation is weather-dependent and can fluctuate significantly. Energy procurement teams need reliable forecasts to estimate how much electricity may need to be purchased from the day-ahead market beyond expected renewable generation.

WindScope compares actual wind generation with day-ahead forecasts and provides analytical insights into forecast performance.

The initial analysis covers **January 2026**.

## 2. Business Problem

Energy procurement teams need to understand:

- How accurately is wind generation being forecast?
- How large is the difference between forecast and actual generation?
- When does the forecast overestimate or underestimate actual generation?
- How does forecast performance change over time?

WindScope addresses these questions through an interactive analytics dashboard.

## 3. Key Features

- **Actual vs Forecast Comparison:** Visualises actual wind generation against day-ahead forecasts.
- **Forecast Accuracy Metrics:** Calculates MAE, RMSE and MAPE.
- **Forecast Error Analysis:** Identifies the difference between forecast and actual generation.
- **Overforecast and Underforecast Analysis:** Counts hours when forecast generation is higher or lower than actual generation.
- **Date Range Filtering:** Allows users to analyse selected delivery periods.
- **Hourly Data Table:** Displays actual generation, forecast generation and forecast errors.
- **CSV Export:** Exports hourly analytical data for further analysis.
- **Responsive Dashboard:** Provides a clean interface for analysing renewable generation performance.

## 4. Technology Stack

| Layer | Technologies |
|---|---|
| Frontend | React, TypeScript, Vite |
| UI | CSS, Recharts, Lucide React |
| Backend | Python, FastAPI |
| Data Processing | Pandas, NumPy |
| Testing | Pytest |
| Data Source | Elexon BMRS API |
| Containerisation | Docker, Docker Compose |
| Frontend Deployment | Vercel |
| Backend Deployment | Render |
| Version Control | Git, GitHub |

## 5. Data Sources

WindScope uses official Elexon BMRS datasets:

**FUELHH – Actual Generation**
- Retrieves half-hourly electricity generation data.
- Filters records for the WIND fuel type.
- Used to calculate actual wind generation.

Documentation: https://bmrs.elexon.co.uk/api-documentation/endpoint/datasets/FUELHH/stream

**WINDFOR – Wind Generation Forecast**
- Retrieves wind generation forecast records.
- Includes delivery time and publication time.
- Used to identify the appropriate day-ahead forecast.

Documentation: https://bmrs.elexon.co.uk/api-documentation/endpoint/datasets/WINDFOR/stream

## 6. Forecast Selection Methodology

The platform follows these analytical steps:

1. Retrieve actual wind generation from FUELHH.
2. Retrieve wind generation forecasts from WINDFOR.
3. Aggregate half-hourly actual generation into hourly values using the average of the two half-hourly records.
4. Associate forecasts with their delivery periods.
5. Select the latest forecast published before **11:00 UTC on the day before the delivery date**.
6. Match selected forecasts with actual generation using hourly delivery timestamps.
7. Calculate forecast errors and accuracy metrics.

**Important:** The 11:00 UTC cutoff is an analytical assumption adopted for this project. It is not presented as an official market rule.

## 7. Forecast Evaluation Metrics

### Mean Absolute Error (MAE)

Measures the average absolute difference between forecast and actual generation.

MAE = Mean(|Forecast − Actual|)

### Root Mean Square Error (RMSE)

Measures forecast error while penalising larger errors more heavily.

RMSE = √Mean((Forecast − Actual)²)

### Mean Absolute Percentage Error (MAPE)

Measures average absolute percentage error.

MAPE = Mean(|Actual − Forecast| / |Actual|) × 100

Zero actual values are excluded from the MAPE calculation.

### Forecast Error

Forecast Error = Forecast Generation − Actual Generation

- Positive error: Overforecasting.
- Negative error: Underforecasting.
- Zero error: Exact match.

## 8. January 2026 Analytical Results

The following results were obtained from the January 2026 analysis:

| Metric | Result |
|---|---:|
| Actual Records | 1,488 |
| Forecast Records Retrieved | 18,688 |
| Selected Forecast Records | 744 |
| Matched Hourly Records | 744 |
| Mean Absolute Error | 2,122.81 MW |
| Root Mean Square Error | 2,616.69 MW |
| Mean Absolute Percentage Error | 22.06% |
| Overforecasted Hours | 628 |
| Underforecasted Hours | 116 |
| Exactly Matched Hours | 0 |

These results represent the selected forecast and actual generation comparisons for January 2026.

## 9. Project Architecture

```text
wind-forecast-analytics/
│
├── backend/
│   ├── analytics/
│   ├── services/
│   ├── schemas/
│   ├── tests/
│   ├── main.py
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
│
├── docs/
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

### Data Flow

```text
Elexon BMRS API
       |
       v
Python FastAPI Backend
       |
       v
Data Alignment & Forecast Selection
       |
       v
Forecast Evaluation Metrics
       |
       v
REST API Response
       |
       v
React + TypeScript Dashboard
       |
       v
Charts, KPIs, Hourly Table & CSV
```

## 10. Run Locally

### Prerequisites

- Python 3.12
- Node.js and npm
- Git

### Clone the Repository

```bash
git clone https://github.com/safwanshaikh053/wind-analytics-platform.git

cd wind-analytics-platform
```

### Backend Setup

Open a terminal:

```bash
cd backend

py -3.12 -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

python -m uvicorn main:app --reload
```

Backend URL:

http://localhost:8000

API documentation:

http://localhost:8000/docs

### Frontend Setup

Open another terminal:

```bash
cd frontend

npm install
```

Create a `.env` file inside the frontend directory:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

Start the frontend:

```bash
npm run dev
```

Frontend URL:

http://localhost:5173

## 11. Run Using Docker

Make sure Docker Desktop is running.

From the project root:

```bash
docker compose up --build
```

Frontend:

http://localhost:5173

Backend:

http://localhost:8000

Stop the containers:

```bash
docker compose down
```

## 12. Deployment

WindScope is deployed using separate frontend and backend services.

| Component | Platform | URL |
|---|---|---|
| Frontend | Vercel | https://wind-analytics-platform.vercel.app/ |
| Backend | Render | https://wind-analytics-backend.onrender.com/ |

The frontend communicates with the backend through the deployed REST API.

The backend uses a `FRONTEND_URL` environment variable to configure production CORS.

**Note:** The Render free instance may spin down after inactivity, causing a delay on the first request.

## 13. Testing

Backend tests are implemented using Pytest.

Run the test suite:

```bash
cd backend

pytest
```

The project has passed its implemented backend test suite during development.

## 14. Limitations and Future Improvements

- Extend analysis to additional months and delivery periods.
- Introduce automated data caching to reduce repeated API requests.
- Improve handling and reporting of missing half-hourly records.
- Make the forecast publication cutoff configurable.
- Add historical forecast accuracy comparisons.
- Introduce additional analytical insights for energy procurement teams.
- Add automated scheduled data refresh.

**Analytical limitation:** Forecast error measures the difference between wind generation forecast and actual wind generation. It does not independently calculate the exact additional electricity procurement requirement, which would also require demand and other generation data.

## 15. AI Tools Disclosure

The following AI tools were used during the development of WindScope:

- **ChatGPT (GPT):** Used for technical guidance, architecture discussions, debugging assistance, documentation preparation and implementation support.
- **GitHub Copilot:** Used for code suggestions, code completion and development assistance.

AI tools were used as development aids. The implementation, integration, testing and deployment of the application were carried out as part of the project development process.

---

**WindScope – Renewable Energy Intelligence**

Built to analyse, understand and evaluate day-ahead wind generation forecasts.