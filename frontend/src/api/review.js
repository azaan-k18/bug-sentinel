// frontend/src/api/review.js
import api from './client';

// Fetch queue
export const fetchReviewQueue = async () => {
  const res = await api.get('/review/queue');
  return res.data.queue;
};

// Fetch single failure details
export const fetchFailureDetail = async (id) => {
  const res = await api.get(`/review/${id}`);
  return res.data;
};

// Submit human label
export const submitHumanLabel = async (id, payload) => {
  const res = await api.post(`/review/${id}/label`, payload);
  return res.data;
};