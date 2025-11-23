import React, { useEffect, useState } from "react";
import { fetchClusterTimeseries } from "../api/trends";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function ClusterTrendView({ id, onBack }) {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchClusterTimeseries(id).then(setData);
  }, [id]);

  if (!data) return <div className="p-6">Loading trend...</div>;

  return (
    <div className="p-6 space-y-5">
      <button className="text-blue-600" onClick={onBack}>← Back</button>

      <h1 className="text-2xl font-bold">Cluster #{id} Trend</h1>

      <p className="text-gray-700">{data.representative_message}</p>

      <div className="bg-white p-4 rounded-xl shadow">
        <h2 className="font-semibold mb-3">Failure Count (Daily)</h2>

        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data.timeseries}>
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line dataKey="count" stroke="#2563eb" />
            <Line dataKey="moving_avg_7d" stroke="#16a34a" />
            <Line dataKey="moving_avg_30d" stroke="#f59e0b" />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
