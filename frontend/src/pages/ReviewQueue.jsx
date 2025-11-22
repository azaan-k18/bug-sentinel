// frontend/src/pages/ReviewQueue.jsx
import React, { useEffect, useState } from "react";
import { fetchReviewQueue } from "../api/review";

export default function ReviewQueue({ onSelect }) {
  const [queue, setQueue] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        setLoading(true);
        const data = await fetchReviewQueue();
        setQueue(data);
      } catch (e) {
        console.error("Failed to load review queue:", e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading) {
    return <div className="p-6 text-gray-500">Loading review queue...</div>;
  }

  if (queue.length === 0) {
    return <div className="p-6 text-gray-500">No failures need review..</div>;
  }

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold">Review Queue</h1>

      <div className="space-y-3">
        {queue.map((item) => (
          <div
            key={item.id}
            className="bg-white p-4 rounded-xl shadow flex justify-between items-center"
          >
            <div>
              <p className="text-lg font-semibold">{item.test_name || "Unknown Test"}</p>
              <p className="text-gray-600 text-sm">{item.summary}</p>
            </div>

            <button
              onClick={() => onSelect(item.id)}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg"
            >
              Review
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
