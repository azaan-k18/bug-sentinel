export default function Navbar() {
    return (
        <header className="w-full bg-gray-800 text-white p-4 shadow">
            <div className="max-w-7xl mx-auto flex items-center justify-between">

                {/* Left section - Project Title */}
                <div>
                    <h1 className="text-2xl font-bold tracking-wide">
                        SentinelQA
                    </h1>
                    <p className="text-sm text-gray-300 -mt-1">
                        by <span className="font-semibold">Azaan Khan</span>
                    </p>
                </div>

                {/* Right section - tagline */}
                <div className="text-right">
                    <p className="text-sm text-gray-300 italic">
                        Converting raw Jenkins artifacts into presentable dashboards.
                    </p>
                </div>
            </div>
        </header>
    );
}