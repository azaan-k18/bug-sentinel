import React, { useEffect, useState } from "react";
import { fetchTrendingClusters } from "../api/trends";

export default function TrendingClusters({ onSelect }) {
  const [clusters, setClusters] = useState([]);

  useEffect(() => {
    fetchTrendingClusters().then(setClusters);
  }, []);

  return (
    <div className="p-6 space-y-5">
      <h1 className="text-2xl font-bold">Trending Clusters</h1>

      {clusters.map((c) => (
        <div
          key={c.cluster_id}
          onClick={() => onSelect(c.cluster_id)}
          className="bg-white p-4 shadow rounded-xl cursor-pointer hover:bg-gray-50"
        >
          <p className="font-semibold text-lg">Cluster #{c.cluster_id}</p>
          <p className="text-gray-600 text-sm">{c.representative_message}</p>

          <div className="flex justify-between mt-2">
            <span className="text-sm">Total failures: {c.total_failures}</span>
            {c.has_spike && (
              <span className="text-red-600 font-bold">🔥 Spike detected</span>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}