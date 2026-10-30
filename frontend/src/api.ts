
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export interface HourlyData {
  delivery_time: string;
  actual_generation: number;
  forecast_generation: number;
  error: number;
  absolute_error: number;
}

export interface AnalyticsResponse {
  start_date: string;
  end_date: string;
  actual_records: number;
  forecast_records: number;
  selected_forecasts: number;
  metrics: {
    mae: number | null;
    rmse: number | null;
    mape: number | null;
    records_count: number;
    hourly_data: HourlyData[];
  };
}

export async function fetchAnalytics(
  startDate: string,
  endDate: string
): Promise<AnalyticsResponse> {
  const params = new URLSearchParams({
    start_date: startDate,
    end_date: endDate,
  });

  const response = await fetch(
    `${API_BASE_URL}/api/analytics?${params.toString()}`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch wind analytics");
  }

  return response.json();
}
