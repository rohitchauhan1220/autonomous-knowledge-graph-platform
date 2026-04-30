async function getAnalyticsSnapshot() {
  return API.get("/api/dashboard/metrics");
}
