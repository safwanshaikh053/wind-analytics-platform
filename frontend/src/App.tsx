
import { useEffect, useState } from "react";
import {
  Activity,
  Wind,
  Target,
  TrendingUp,
  RefreshCw,
  Download,
} from "lucide-react";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { fetchAnalytics, type AnalyticsResponse } from "./api";
import "./App.css";

function App() {
 const [data, setData] = useState<AnalyticsResponse | null>(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState("");

const [startDate, setStartDate] = useState("2026-01-01");
const [endDate, setEndDate] = useState("2026-01-31");
const [currentPage, setCurrentPage] = useState(1);
const pageSize = 10;
  async function loadAnalytics() {
  try {
    setLoading(true);
    setError("");
setCurrentPage(1);
    const result = await fetchAnalytics(startDate, endDate);

    setData(result);
  } catch (err) {
    setError(
      err instanceof Error ? err.message : "Something went wrong"
    );
  } finally {
    setLoading(false);
  }
}

  const exportToCSV = () => {
    if (!data) return;

    const headers = [
      "Delivery Time UTC",
      "Actual Generation (MW)",
      "Forecast Generation (MW)",
      "Forecast Error (MW)",
      "Absolute Error (MW)",
    ];

    const rows = data.metrics.hourly_data.map((item) => [
      item.delivery_time,
      item.actual_generation,
      item.forecast_generation,
      item.error,
      item.absolute_error,
    ]);

    const csvContent = [
      headers.join(","),
      ...rows.map((row) => row.join(",")),
    ].join("\n");

    const blob = new Blob(["\uFEFF" + csvContent], {
      type: "text/csv;charset=utf-8;",
    });

    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");

    link.href = url;
    link.download = `wind-analytics-${data.start_date}-to-${data.end_date}.csv`;

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(url);
  };

  useEffect(() => {
    loadAnalytics();
  }, []);

  if (loading) {
    return <div className="status-screen">Loading wind analytics...</div>;
  }

  if (error || !data) {
    return (
      <div className="status-screen">
        <p>{error || "No analytics data available"}</p>
        <button onClick={loadAnalytics}>Try again</button>
      </div>
    );
  }

  const metrics = data.metrics;
const totalPages = Math.ceil(metrics.hourly_data.length / pageSize);

const paginatedData = metrics.hourly_data.slice(
  (currentPage - 1) * pageSize,
  currentPage * pageSize
);
  const overforecasted = metrics.hourly_data.filter(
  (item) => item.error > 0
).length;

const underforecasted = metrics.hourly_data.filter(
  (item) => item.error < 0
).length;

const matched = metrics.hourly_data.filter(
  (item) => item.error === 0
).length;

  const chartData = metrics.hourly_data.map((item) => ({
    ...item,
    time: new Date(item.delivery_time).toLocaleString("en-GB", {
      day: "2-digit",
      month: "short",
      hour: "2-digit",
      minute: "2-digit",
      timeZone: "UTC",
    }),
  }));

  return (
    <main className="dashboard">
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon">
            <Wind size={25} />
          </div>
          <div>
            <h1>WindScope</h1>
            <p>Renewable Energy Intelligence</p>
          </div>
        </div>

        <div className="header-right">
          <span className="live-indicator">Data connected</span>
          <button className="refresh-button" onClick={loadAnalytics}>
            <RefreshCw size={16} />
            Refresh
          </button>
        </div>
      </header>

      <section className="page-heading">
        <div>
          <p className="eyebrow">ENERGY TRADING ANALYTICS</p>
          <h2>Wind Generation Overview</h2>
          <p className="subtitle">
            Actual generation versus day-ahead forecast performance
          </p>
        </div>
       <div className="date-filters">
  <div className="date-input-group">
    <label htmlFor="start-date">From</label>
    <input
      id="start-date"
      type="date"
      value={startDate}
      min="2026-01-01"
      max="2026-01-31"
      onChange={(e) => setStartDate(e.target.value)}
    />
  </div>

  <div className="date-input-group">
    <label htmlFor="end-date">To</label>
    <input
      id="end-date"
      type="date"
      value={endDate}
      min={startDate}
      max="2026-01-31"
      onChange={(e) => setEndDate(e.target.value)}
    />
  </div>

  <button
    className="apply-button"
    onClick={loadAnalytics}
    disabled={loading || startDate > endDate}
  >
    Apply Filters
  </button>
</div>
      </section>

      <section className="metrics-grid">
        <article className="metric-card">
          <div className="metric-heading">
            <span>Mean Absolute Error</span>
            <Target size={20} />
          </div>
          <h3>{metrics.mae?.toLocaleString("en-GB") ?? "N/A"}</h3>
          <p>MW · Lower is better</p>
        </article>

        <article className="metric-card">
          <div className="metric-heading">
            <span>Root Mean Square Error</span>
            <Activity size={20} />
          </div>
          <h3>{metrics.rmse?.toLocaleString("en-GB") ?? "N/A"}</h3>
          <p>MW · Penalises larger errors</p>
        </article>

        <article className="metric-card">
          <div className="metric-heading">
            <span>Mean Absolute Percentage Error</span>
            <TrendingUp size={20} />
          </div>
          <h3>{metrics.mape?.toFixed(2) ?? "N/A"}%</h3>
          <p>Percentage · Zero actuals excluded</p>
        </article>

        <article className="metric-card">
          <div className="metric-heading">
            <span>Matched Hourly Records</span>
            <Wind size={20} />
          </div>
          <h3>{metrics.records_count.toLocaleString("en-GB")}</h3>
          <p>Hourly forecast and actual pairs</p>
        </article>
      </section>

<section className="metrics-grid performance-grid">
  <article className="metric-card">
    <div className="metric-heading">
      <span>Overforecasted Hours</span>
      <TrendingUp size={20} />
    </div>
    <h3>{overforecasted}</h3>
    <p>Forecast higher than actual</p>
  </article>

  <article className="metric-card">
    <div className="metric-heading">
      <span>Underforecasted Hours</span>
      <Activity size={20} />
    </div>
    <h3>{underforecasted}</h3>
    <p>Forecast lower than actual</p>
  </article>

  <article className="metric-card">
    <div className="metric-heading">
      <span>Exactly Matched Hours</span>
      <Target size={20} />
    </div>
    <h3>{matched}</h3>
    <p>Forecast equals actual</p>
  </article>
</section>

      <section className="chart-card">
        <div className="section-heading">
          <div>
            <h3>Actual vs Forecast Generation</h3>
           <p>
  Hourly wind generation from {data.start_date} to {data.end_date} · UTC
</p>
          </div>
          <span className="unit-label">MW</span>
        </div>

        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis
                dataKey="time"
                minTickGap={50}
                tick={{ fontSize: 11 }}
              />
              <YAxis tick={{ fontSize: 11 }} />
              <Tooltip />
              <Legend />
              <Line
                type="monotone"
                dataKey="actual_generation"
                name="Actual Generation"
                stroke="#16a085"
                strokeWidth={2}
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="forecast_generation"
                name="Day-Ahead Forecast"
                stroke="#6366f1"
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </section>

<section className="chart-card">
  <div className="section-heading">
    <div>
      <h3>Forecast Error Analysis</h3>
      <p>Hourly difference between forecast and actual generation</p>
    </div>
    <span className="unit-label">MW</span>
  </div>

  <div className="chart-container">
    <ResponsiveContainer width="100%" height="100%">
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" vertical={false} />
        <XAxis
          dataKey="time"
          minTickGap={50}
          tick={{ fontSize: 11 }}
        />
        <YAxis tick={{ fontSize: 11 }} />
        <Tooltip />
        <Legend />
        <Line
          type="monotone"
          dataKey="error"
          name="Forecast Error"
          stroke="#e67e22"
          strokeWidth={2}
          dot={false}
        />
      </LineChart>
    </ResponsiveContainer>
  </div>
</section>

<section className="table-card">
  <div className="section-heading">
    <div>
      <h3>Hourly Forecast Data</h3>
      <p>Detailed actual and forecast generation comparison</p>
    </div>

    <div className="table-actions">
      <span className="unit-label">
        {metrics.records_count} Records
      </span>

      <button className="export-button" onClick={exportToCSV}>
        <Download size={16} />
        Export CSV
      </button>
    </div>
  </div>

  <div className="table-wrapper">
    <table className="data-table">
      <thead>
        <tr>
          <th>Delivery Time (UTC)</th>
          <th>Actual (MW)</th>
          <th>Forecast (MW)</th>
          <th>Forecast Error (MW)</th>
          <th>Absolute Error (MW)</th>
        </tr>
      </thead>

      <tbody>
        {paginatedData.map((item) => (
          <tr key={item.delivery_time}>
            <td>
              {new Date(item.delivery_time).toLocaleString("en-GB", {
                day: "2-digit",
                month: "short",
                year: "numeric",
                hour: "2-digit",
                minute: "2-digit",
                timeZone: "UTC",
              })}
            </td>
            <td>{item.actual_generation.toLocaleString("en-GB")}</td>
            <td>{item.forecast_generation.toLocaleString("en-GB")}</td>
            <td
              className={
                item.error > 0
                  ? "positive-error"
                  : item.error < 0
                  ? "negative-error"
                  : ""
              }
            >
              {item.error.toLocaleString("en-GB")}
            </td>
            <td>{item.absolute_error.toLocaleString("en-GB")}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
  
<div className="pagination">
  <button
    onClick={() => setCurrentPage((page) => page - 1)}
    disabled={currentPage === 1}
  >
    Previous
  </button>

  <span>
    Page {currentPage} of {totalPages}
  </span>

  <button
    onClick={() => setCurrentPage((page) => page + 1)}
    disabled={currentPage === totalPages}
  >
    Next
  </button>
</div>

</section>

      <footer className="dashboard-footer">
        <span>Source: Elexon BMRS · FUELHH and WINDFOR</span>
        <span>Day-ahead cutoff assumption: 11:00 UTC</span>
      </footer>
    </main>
  );
}

export default App;
