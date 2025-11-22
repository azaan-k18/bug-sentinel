// frontend/src/pages/ReviewOne.jsx
import React, { useEffect, useState } from "react";
import { fetchFailureDetail, submitHumanLabel } from "../api/review";

const LABELS = [
  "locator_failure",
  "timeout_error",
  "assertion_failure",
  "network_error",
  "environment_issue",
  "application_crash",
  "unknown",
];

export default function ReviewOne({ id, onBack }) {
  const [data, setData] = useState(null);
  const [label, setLabel] = useState("");
  const [notes, setNotes] = useState("");
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    async function load() {
      const detail = await fetchFailureDetail(id);
      setData(detail);
    }
    load();
  }, [id]);

  const saveLabel = async () => {
    if (!label) {
      alert("Select a label before saving!");
      return;
    }

    setSaving(true);

    try {
      await submitHumanLabel(id, {
        label,
        reviewer: "Azaan",
        notes,
      });
      onBack();
    } catch (e) {
      console.error("Failed to save label:", e);
      alert("Error saving label");
    } finally {
      setSaving(false);
    }
  };

  if (!data) return <div className="p-6 text-gray-500">Loading...</div>;

  return (
    <div className="p-6 space-y-6">
      <button className="text-blue-600 mb-4" onClick={onBack}>
        ← Back to Queue
      </button>

      <h1 className="text-2xl font-bold">Review Failure #{id}</h1>

      <div className="bg-white p-4 rounded-xl shadow space-y-2">
        <p><strong>Test:</strong> {data.test_name}</p>
        <p><strong>Platform:</strong> {data.platform}</p>
        <p><strong>Website:</strong> {data.website}</p>
        <p><strong>Normalized:</strong> {data.normalized}</p>

        <p><strong>Model prediction:</strong>  
          <span className="ml-2 text-purple-700 font-medium">
            {data.model_label || "N/A"} ({data.model_confidence ?? "?"})
          </span>
        </p>

        <p><strong>Error message (full):</strong></p>
        <pre className="p-2 bg-gray-50 rounded-md max-h-64 overflow-auto text-sm">
          {data.error_message}
        </pre>
      </div>

      <div className="bg-white p-4 rounded-xl shadow space-y-4">
        <h2 className="text-lg font-semibold">Assign Human Label</h2>

        <select
          className="border p-2 w-full"
          value={label}
          onChange={(e) => setLabel(e.target.value)}
        >
          <option value="">Select a label</option>
          {LABELS.map((l) => (
            <option key={l} value={l}>{l}</option>
          ))}
        </select>

        <textarea
          className="border p-2 w-full"
          rows={4}
          placeholder="Optional notes..."
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
        />

        <button
          disabled={saving}
          onClick={saveLabel}
          className="px-4 py-2 bg-green-600 text-white rounded-lg"
        >
          {saving ? "Saving..." : "Save Label"}
        </button>
      </div>
    </div>
  );
}