import React, { useState } from "react";
import Navbar from "./components/Navbar";

import Overview from "./pages/Overview";
import ReviewQueue from "./pages/ReviewQueue";
import ReviewOne from "./pages/ReviewOne";

import TrendingClusters from "./pages/TrendingClusters";
import ClusterTrendView from "./pages/ClusterTrendView";
import SpikeAlerts from "./pages/SpikeAlerts";
import ClusterRCA from "./pages/ClusterRCA";

export default function App() {
  const [view, setView] = useState("overview");
  const [selectedId, setSelectedId] = useState(null);        // for Failure ID (review)
  const [selectedCluster, setSelectedCluster] = useState(null); // for Cluster ID (trends/rca)

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />

      {/* Simple navigation bar */}
      <div className="p-4 bg-white shadow flex flex-wrap gap-4">

        {/* Overview */}
        <button
          className={`px-4 py-2 rounded ${
            view === "overview" ? "bg-gray-800 text-white" : "bg-gray-200"
          }`}
          onClick={() => setView("overview")}
        >
          Overview
        </button>

        {/* Review Queue */}
        <button
          className={`px-4 py-2 rounded ${
            view === "queue" || view === "detail"
              ? "bg-gray-800 text-white"
              : "bg-gray-200"
          }`}
          onClick={() => {
            setSelectedId(null);
            setView("queue");
          }}
        >
          Review Queue
        </button>

        {/* Trending Clusters */}
        <button
          className={`px-4 py-2 rounded ${
            view === "trending" || view === "cluster_trend"
              ? "bg-gray-800 text-white"
              : "bg-gray-200"
          }`}
          onClick={() => {
            setSelectedCluster(null);
            setView("trending");
          }}
        >
          Trending Clusters
        </button>

        {/* Spike Alerts */}
        <button
          className={`px-4 py-2 rounded ${
            view === "spikes" || view === "cluster_rca"
              ? "bg-gray-800 text-white"
              : "bg-gray-200"
          }`}
          onClick={() => {
            setSelectedCluster(null);
            setView("spikes");
          }}
        >
          Spike Alerts
        </button>
      </div>

      {/* Views */}
      <div className="mt-4">

        {/* Overview */}
        {view === "overview" && <Overview />}

        {/* Review Queue */}
        {view === "queue" && (
          <ReviewQueue
            onSelect={(id) => {
              setSelectedId(id);
              setView("detail");
            }}
          />
        )}

        {/* Review Failure Detail */}
        {view === "detail" && (
          <ReviewOne
            id={selectedId}
            onBack={() => {
              setSelectedId(null);
              setView("queue");
            }}
          />
        )}

        {/* Trending Clusters List */}
        {view === "trending" && (
          <TrendingClusters
            onSelect={(clusterId) => {
              setSelectedCluster(clusterId);
              setView("cluster_trend");
            }}
          />
        )}

        {/* Cluster Trend Chart */}
        {view === "cluster_trend" && (
          <ClusterTrendView
            id={selectedCluster}
            onBack={() => setView("trending")}
          />
        )}

        {/* Spike Alerts */}
        {view === "spikes" && (
          <SpikeAlerts
            onSelect={(clusterId) => {
              setSelectedCluster(clusterId);
              setView("cluster_rca");
            }}
          />
        )}

        {/* RCA: Root Cause Analysis for Cluster */}
        {view === "cluster_rca" && (
          <ClusterRCA
            id={selectedCluster}
            onBack={() => setView("spikes")}
          />
        )}
      </div>
    </div>
  );
}