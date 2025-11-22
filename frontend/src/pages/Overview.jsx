import { useEffect, useState } from 'react';
import { fetchOverviewStats } from '../api/dashboard';


export default function Overview() {
    const [stats, setStats] = useState(null);


    useEffect(() => {
        fetchOverviewStats().then(data => setStats(data));
    }, []);


    if (!stats) return <p>Loading...</p>;


    return (
        <div className="p-6">
            <h2 className="text-2xl font-bold mb-4">Overview</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 bg-white shadow rounded">
                    <h3 className="text-gray-500">Total Bugs (Quarter)</h3>
                    <p className="text-3xl font-bold">{stats.total_bugs}</p>
                </div>


                <div className="p-4 bg-white shadow rounded">
                    <h3 className="text-gray-500">Pass Rate</h3>
                    <p className="text-3xl font-bold">{stats.pass_rate}%</p>
                </div>


                <div className="p-4 bg-white shadow rounded">
                    <h3 className="text-gray-500">False Positive %</h3>
                    <p className="text-3xl font-bold">{stats.false_positive_rate}%</p>
                </div>
            </div>
        </div>
    );
}