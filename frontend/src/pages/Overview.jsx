import React, { useEffect, useState } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
} from "recharts";

const API_BASE = "http://127.0.0.1:8000/api/v1/dashboard";

const COLORS = ["#4F46E5", "#16A34A", "#F59E0B", "#EF4444", "#6366F1"];

export default function Overview() {
  const [overview, setOverview] = useState(null);
  const [topIssues, setTopIssues] = useState([]);
  const [modelHealth, setModelHealth] = useState(null);

  useEffect(() => {
    async function loadData() {
      try {
        const [overviewRes, topIssuesRes, modelHealthRes] = await Promise.all([
          axios.get(`${API_BASE}/overview`),
          axios.get(`${API_BASE}/top-issues`),
          axios.get(`${API_BASE}/model-health`),
        ]);

        setOverview(overviewRes.data);
        setTopIssues(topIssuesRes.data.top_issues);
        setModelHealth(modelHealthRes.data);
      } catch (e) {
        console.error("Dashboard API error:", e);
      }
    }
    loadData();
  }, []);

  if (!overview) {
    return <div className="text-center mt-10 text-gray-500">Loading dashboard...</div>;
  }

  return (
    <div className="p-6 space-y-8">
      <h1 className="text-3xl font-bold mb-4">Dashboard Overview</h1>

      {/* METRIC CARDS */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

        <div className="bg-white shadow rounded-xl p-6">
          <p className="text-gray-500">Total Failures</p>
          <h2 className="text-3xl font-bold mt-2">{overview.total_bugs}</h2>
        </div>

        <div className="bg-white shadow rounded-xl p-6">
          <p className="text-gray-500">Total Runs</p>
          <h2 className="text-3xl font-bold mt-2">{overview.total_runs}</h2>
        </div>

        <div className="bg-white shadow rounded-xl p-6">
          <p className="text-gray-500">Pass Rate</p>
          <h2 className="text-3xl font-bold mt-2">{overview.pass_rate}%</h2>
        </div>

      </div>

      {/* ROW 2 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">

        {/* TOP ISSUES BAR CHART */}
        <div className="bg-white p-6 shadow rounded-xl">
          <h2 className="text-xl font-semibold mb-4">Top Recurring Issues</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={topIssues}>
              <XAxis dataKey="summary" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="count" fill="#4F46E5" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* MODEL HEALTH PIE CHART */}
        <div className="bg-white p-6 shadow rounded-xl">
          <h2 className="text-xl font-semibold mb-4">Model Health</h2>

          {modelHealth ? (
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={[
                    { name: "Labeled", value: modelHealth.total_labeled },
                    { name: "Low Confidence", value: modelHealth.low_confidence },
                  ]}
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                  label
                >
                  {COLORS.map((color, index) => (
                    <Cell key={index} fill={color} />
                  ))}
                </Pie>
                <Legend />
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : (
            <p>No model data available</p>
          )}
        </div>
      </div>
    </div>
  );
}
