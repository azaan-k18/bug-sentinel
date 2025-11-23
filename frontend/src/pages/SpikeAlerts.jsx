import React, { useEffect, useState } from "react";
import { fetchRecentSpikes } from "../api/trends";

export default function SpikeAlerts({ onSelect }) {
  const [spikes, setSpikes] = useState([]);

  useEffect(() => {
    fetchRecentSpikes().then(setSpikes);
  }, []);

  if (spikes.length === 0)
    return <div className="p-6 text-gray-600">No spikes detected.</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Recent Spike Alerts</h1>

      <div className="space-y-4">
        {spikes.map((s, i) => (
          <div
            key={i}
            onClick={() => onSelect(s.cluster_id)}
            className="bg-white p-4 rounded-xl shadow cursor-pointer hover:bg-gray-50"
          >
            <p className="font-semibold text-lg">Cluster #{s.cluster_id}</p>
            <p className="text-gray-600 text-sm">{s.representative_message}</p>

            <p className="text-red-600 mt-2">
              🔥 Spike on {s.date} — {s.failure_count} failures
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}