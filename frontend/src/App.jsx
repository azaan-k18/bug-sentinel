import Navbar from './components/Navbar';
import Overview from './pages/Overview';


export default function App() {
    return (
        <div className="min-h-screen bg-gray-100">
            <Navbar />
            <Overview />
        </div>
    );
}