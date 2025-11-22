import api from './client';

export const fetchOverviewStats = async () => {
const res = await api.get('/dashboard/overview');
return res.data;
};