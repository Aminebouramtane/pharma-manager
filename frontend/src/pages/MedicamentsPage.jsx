import { useState, useEffect } from 'react';
import { FaPlus, FaTimes, FaTrash, FaExclamationTriangle, FaSave } from 'react-icons/fa';
import { fetchMedicaments, fetchMedicamentsAlertes, createMedicament, updateMedicament, deleteMedicament } from '../api/medicamentsApi';
import { fetchCategories } from '../api/categoriesApi';

function MedicamentsPage() {
  const [medicaments, setMedicaments] = useState([]);
  const [categories, setCategories] = useState([]);
  const [alertes, setAlertes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    nom: '',
    dci: '',
    categorie: '',
    forme: 'comprime',
    dosage: '',
    prix_achat: '',
    prix_vente: '',
    stock_actuel: 0,
    stock_minimum: 10,
    date_expiration: '',
    ordonnance_requise: false
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [medsData, catsData, alertsData] = await Promise.all([
        fetchMedicaments(),
        fetchCategories(),
        fetchMedicamentsAlertes()
      ]);
      setMedicaments(medsData.results || medsData);
      setCategories(catsData.results || catsData);
      setAlertes(alertsData);
      setError(null);
    } catch (err) {
      setError('Erreur lors du chargement des données');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Convert numeric strings to numbers
      const dataToSend = {
        ...formData,
        categorie: parseInt(formData.categorie),
        prix_achat: parseFloat(formData.prix_achat),
        prix_vente: parseFloat(formData.prix_vente),
        stock_actuel: parseInt(formData.stock_actuel),
        stock_minimum: parseInt(formData.stock_minimum)
      };
      
      await createMedicament(dataToSend);
      setShowForm(false);
      resetForm();
      loadData();
      setError(null);
    } catch (err) {
      const errorMessage = err.response?.data?.detail 
        || Object.entries(err.response?.data || {}).map(([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`).join('; ')
        || 'Erreur lors de la création du médicament';
      setError(errorMessage);
      console.error('Erreur détaillée:', err.response?.data);
    }
  };

  const handleDelete = async (id) => {
    const medicament = medicaments.find(m => m.id === id);
    const confirmed = window.confirm(`Êtes-vous sûr de vouloir supprimer le médicament "${medicament?.nom}" ?`);
    
    if (confirmed) {
      try {
        await deleteMedicament(id);
        loadData();
      } catch (err) {
        setError('Erreur lors de la suppression du médicament');
        console.error(err);
      }
    }
  };

  const resetForm = () => {
    setFormData({
      nom: '',
      dci: '',
      categorie: '',
      forme: 'comprime',
      dosage: '',
      prix_achat: '',
      prix_vente: '',
      stock_actuel: 0,
      stock_minimum: 10,
      date_expiration: '',
      ordonnance_requise: false
    });
  };

  if (loading) {
    return <div className="loading"><div className="spinner"></div></div>;
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1 className="page-title" style={{ marginBottom: 0 }}>Médicaments</h1>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? <><FaTimes /> Annuler</> : <><FaPlus /> Nouveau médicament</>}
        </button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      {alertes.length > 0 && (
        <div className="alert alert-warning">
          <FaExclamationTriangle /> {alertes.length} médicament(s) en alerte de stock
        </div>
      )}

      {showForm && (
        <div className="card">
          <h2 className="card-title">Nouveau médicament</h2>
          <form onSubmit={handleSubmit}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
              <div className="form-group">
                <label className="form-label">Nom *</label>
                <input
                  type="text"
                  className="form-input"
                  value={formData.nom}
                  onChange={(e) => setFormData({ ...formData, nom: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">DCI</label>
                <input
                  type="text"
                  className="form-input"
                  value={formData.dci}
                  onChange={(e) => setFormData({ ...formData, dci: e.target.value })}
                />
              </div>

              <div className="form-group">
                <label className="form-label">Catégorie *</label>
                <select
                  className="form-select"
                  value={formData.categorie}
                  onChange={(e) => setFormData({ ...formData, categorie: e.target.value })}
                  required
                >
                  <option value="">Sélectionner...</option>
                  {categories.map(cat => (
                    <option key={cat.id} value={cat.id}>{cat.nom}</option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Forme *</label>
                <select
                  className="form-select"
                  value={formData.forme}
                  onChange={(e) => setFormData({ ...formData, forme: e.target.value })}
                  required
                >
                  <option value="comprime">Comprimé</option>
                  <option value="gelule">Gélule</option>
                  <option value="sirop">Sirop</option>
                  <option value="injection">Injection</option>
                  <option value="pommade">Pommade</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Dosage *</label>
                <input
                  type="text"
                  className="form-input"
                  value={formData.dosage}
                  onChange={(e) => setFormData({ ...formData, dosage: e.target.value })}
                  placeholder="Ex: 500mg"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Date d'expiration *</label>
                <input
                  type="date"
                  className="form-input"
                  value={formData.date_expiration}
                  onChange={(e) => setFormData({ ...formData, date_expiration: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Prix d'achat *</label>
                <input
                  type="number"
                  step="0.01"
                  className="form-input"
                  value={formData.prix_achat}
                  onChange={(e) => setFormData({ ...formData, prix_achat: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Prix de vente *</label>
                <input
                  type="number"
                  step="0.01"
                  className="form-input"
                  value={formData.prix_vente}
                  onChange={(e) => setFormData({ ...formData, prix_vente: e.target.value })}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Stock actuel *</label>
                <input
                  type="number"
                  className="form-input"
                  value={formData.stock_actuel}
                  onChange={(e) => setFormData({ ...formData, stock_actuel: parseInt(e.target.value) })}
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Stock minimum *</label>
                <input
                  type="number"
                  className="form-input"
                  value={formData.stock_minimum}
                  onChange={(e) => setFormData({ ...formData, stock_minimum: parseInt(e.target.value) })}
                  required
                />
              </div>
            </div>

            <div className="form-group">
              <label style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <input
                  type="checkbox"
                  checked={formData.ordonnance_requise}
                  onChange={(e) => setFormData({ ...formData, ordonnance_requise: e.target.checked })}
                />
                Ordonnance requise
              </label>
            </div>

            <button type="submit" className="btn btn-success">Créer le médicament</button>
          </form>
        </div>
      )}

      <div className="card">
        <h2 className="card-title">Liste des médicaments</h2>
        <div style={{ overflowX: 'auto' }}>
          <table className="table">
            <thead>
              <tr>
                <th>Nom</th>
                <th>Dosage</th>
                <th>Catégorie</th>
                <th>Stock</th>
                <th>Prix</th>
                <th>Statut</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {medicaments.map(med => (
                <tr key={med.id}>
                  <td>{med.nom}</td>
                  <td>{med.dosage}</td>
                  <td>{med.categorie_nom}</td>
                  <td>
                    {med.stock_actuel}
                    {med.est_en_alerte && <span className="badge badge-danger" style={{ marginLeft: '0.5rem' }}>ALERTE</span>}
                  </td>
                  <td>{parseFloat(med.prix_vente).toFixed(2)} DH</td>
                  <td>
                    {med.ordonnance_requise && <span className="badge badge-warning">Ordonnance</span>}
                  </td>
                  <td>
                    <button className="btn btn-danger" onClick={() => handleDelete(med.id)} style={{ fontSize: '0.75rem', padding: '0.25rem 0.5rem' }}>
                      Supprimer
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default MedicamentsPage;
