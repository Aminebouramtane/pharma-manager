import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { FaHome, FaPills, FaShoppingCart, FaHospital } from 'react-icons/fa';
import DashboardPage from './pages/DashboardPage';
import MedicamentsPage from './pages/MedicamentsPage';
import VentesPage from './pages/VentesPage';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        {/* Navigation */}
        <nav className="navbar">
          <div className="nav-container">
            <h1 className="nav-logo"><FaHospital /> PharmaManager</h1>
            <ul className="nav-menu">
              <li><Link to="/" className="nav-link"><FaHome /> Dashboard</Link></li>
              <li><Link to="/medicaments" className="nav-link"><FaPills /> Médicaments</Link></li>
              <li><Link to="/ventes" className="nav-link"><FaShoppingCart /> Ventes</Link></li>
            </ul>
          </div>
        </nav>

        {/* Main Content */}
        <main className="main-content">
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/medicaments" element={<MedicamentsPage />} />
            <Route path="/ventes" element={<VentesPage />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="footer">
          <p>© 2026 SMARTHOLOL — PharmaManager</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;
