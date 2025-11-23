// src/api/rca.js
import api from "./client";

// GET /rca/cluster/:id
export const fetchClusterRCA = async (id) => {
  const res = await api.get(`/rca/cluster/${id}`);
  return res.data;
};
