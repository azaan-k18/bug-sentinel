import React, { useEffect, useState } from "react";
import { fetchClusterRCA } from "../api/rca";

export default function ClusterRCA({ id, onBack }) {
  const [rca, setRca] = useState(null);

  useEffect(() => {
    fetchClusterRCA(id).then(setRca);
  }, [id]);

  if (!rca) return <div className="p-6">Loading RCA...</div>;

  return (
    <div className="p-6 space-y-5">
      <button className="text-blue-600" onClick={onBack}>← Back</button>

      <h1 className="text-2xl font-bold">Cluster #{id} RCA</h1>
      <p className="text-gray-700">{rca.representative_message}</p>

      {/* Top Labels */}
      <div className="bg-white p-4 rounded-xl shadow">
        <h2 className="font-semibold mb-2">Top Labels</h2>
        {rca.top_labels.map((l) => (
          <p key={l.label} className="text-gray-700">
            {l.label}: {l.count}
          </p>
        ))}
      </div>

      {/* Top Tests */}
      <div className="bg-white p-4 rounded-xl shadow">
        <h2 className="font-semibold mb-2">Affected Tests</h2>
        {rca.top_tests.map((t) => (
          <p key={t.test_name} className="text-gray-700">
            {t.test_name} — {t.failures} failures — flakiness:{" "}
            {t.flakiness ? (t.flakiness * 100).toFixed(1) + "%" : "N/A"}
          </p>
        ))}
      </div>
    </div>
  );
}