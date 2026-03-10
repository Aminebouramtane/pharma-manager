import { useState, useEffect } from 'react';
import { FaPills, FaExclamationTriangle, FaShoppingCart } from 'react-icons/fa';
import { fetchMedicaments, fetchMedicamentsAlertes } from '../api/medicamentsApi';
import { fetchVentes } from '../api/ventesApi';

function DashboardPage() {
  const [stats, setStats] = useState({
    totalMedicaments: 0,
    alertes: 0,
    ventesJour: 0,
    loading: true
  });

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [medicaments, alertes, ventes] = await Promise.all([
        fetchMedicaments(),
        fetchMedicamentsAlertes(),
        fetchVentes({ date_debut: new Date().toISOString().split('T')[0] })
      ]);

      setStats({
        totalMedicaments: medicaments.count || medicaments.length || 0,
        alertes: alertes.length || 0,
        ventesJour: ventes.count || ventes.results?.length || 0,
        loading: false
      });
    } catch (error) {
      console.error('Error loading dashboard:', error);
      setStats(prev => ({ ...prev, loading: false }));
    }
  };

  if (stats.loading) {
    return (
      <div className="loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div>
      <h1 className="page-title">Dashboard</h1>

      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">Médicaments en stock</div>
          <div className="stat-value">{stats.totalMedicaments}</div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Alertes de stock</div>
          <div className="stat-value" style={{ color: '#dc2626' }}>
            {stats.alertes}
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Ventes du jour</div>
          <div className="stat-value" style={{ color: '#16a34a' }}>
            {stats.ventesJour}
          </div>
        </div>
      </div>

      <div className="card">
        <h2 className="card-title">Bienvenue sur PharmaManager</h2>
        <p>Système de gestion de pharmacie développé pour SMARTHOLOL</p>
        <p style={{ marginTop: '1rem', color: '#6b7280' }}>
          Utilisez le menu de navigation pour gérer les médicaments et les ventes.
        </p>
      </div>
    </div>
  );
}

export default DashboardPage;
