// src/api/trends.js
import api from "./client";

// GET /trends/clusters?days=30&limit=50
export const fetchTrendingClusters = async () => {
  const res = await api.get("/trends/clusters");
  return res.data;
};

// GET /trends/clusters/:id
export const fetchClusterTimeseries = async (id) => {
  const res = await api.get(`/trends/clusters/${id}`);
  return res.data;
};

// GET /trends/spikes
export const fetchRecentSpikes = async () => {
  const res = await api.get("/trends/spikes");
  return res.data.spikes;
};
