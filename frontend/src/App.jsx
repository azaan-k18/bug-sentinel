import React, { useState } from "react";
import Navbar from './components/Navbar';
import Overview from './pages/Overview';
import ReviewQueue from "./pages/ReviewQueue";
import ReviewOne from "./pages/ReviewOne";

export default function App() {
    const [view, setView] = useState("overview");
    const [selectedId, setSelectedId] = useState(null);

    return (
        <div className="min-h-screen bg-gray-100">
            <Navbar />

            {/* Simple navigation bar */}
            <div className="p-4 bg-white shadow flex gap-4">
                <button
                    className={`px-4 py-2 rounded ${view === "overview" ? "bg-gray-800 text-white" : "bg-gray-200"
                        }`}
                    onClick={() => setView("overview")}
                >
                    Overview
                </button>

                <button
                    className={`px-4 py-2 rounded ${view === "queue" || view === "detail"
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
            </div>

            {/* VIEWS */}
            <div className="mt-4">
                {view === "overview" && <Overview />}

                {view === "queue" && (
                    <ReviewQueue
                        onSelect={(id) => {
                            setSelectedId(id);
                            setView("detail");
                        }}
                    />
                )}

                {view === "detail" && (
                    <ReviewOne
                        id={selectedId}
                        onBack={() => {
                            setSelectedId(null);
                            setView("queue");
                        }}
                    />
                )}
            </div>
        </div>
    );
}