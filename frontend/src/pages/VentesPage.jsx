import { useState, useEffect } from 'react';
import { FaShoppingCart, FaPlus, FaTrash, FaBan, FaTimes } from 'react-icons/fa';
import { fetchVentes, createVente, annulerVente } from '../api/ventesApi';
import { fetchMedicaments } from '../api/medicamentsApi';

function VentesPage() {
  const [ventes, setVentes] = useState([]);
  const [medicaments, setMedicaments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const [showForm, setShowForm] = useState(false);
  const [cart, setCart] = useState([]);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const [ventesData, medsData] = await Promise.all([
        fetchVentes(),
        fetchMedicaments()
      ]);
      setVentes(ventesData.results || ventesData);
      setMedicaments(medsData.results || medsData);
      setError(null);
    } catch (err) {
      setError('Erreur lors du chargement des données');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const addToCart = (medicament) => {
    const existing = cart.find(item => item.medicament.id === medicament.id);
    if (existing) {
      setCart(cart.map(item =>
        item.medicament.id === medicament.id
          ? { ...item, quantite: item.quantite + 1 }
          : item
      ));
    } else {
      setCart([...cart, { medicament, quantite: 1 }]);
    }
  };

  const removeFromCart = (medicamentId) => {
    setCart(cart.filter(item => item.medicament.id !== medicamentId));
  };

  const updateCartQuantity = (medicamentId, quantite) => {
    if (quantite <= 0) {
      removeFromCart(medicamentId);
    } else {
      setCart(cart.map(item =>
        item.medicament.id === medicamentId
          ? { ...item, quantite: parseInt(quantite) }
          : item
      ));
    }
  };

  const calculateTotal = () => {
    return cart.reduce((total, item) =>
      total + (parseFloat(item.medicament.prix_vente) * item.quantite), 0
    ).toFixed(2);
  };

  const handleSubmitVente = async () => {
    if (cart.length === 0) {
      setError('Le panier est vide');
      return;
    }

    try {
      const venteData = {
        notes: '',
        lignes: cart.map(item => ({
          medicament: item.medicament.id,
          quantite: item.quantite,
          prix_unitaire: parseFloat(item.medicament.prix_vente)
        }))
      };

      await createVente(venteData);
      setSuccess('Vente enregistrée avec succès');
      setCart([]);
      setShowForm(false);
      loadData();
      setTimeout(() => setSuccess(null), 3000);
    } catch (err) {
      setError(err.response?.data?.lignes?.[0] || 'Erreur lors de l\'enregistrement de la vente');
      console.error(err);
    }
  };

  const handleAnnulerVente = async (id) => {
    const vente = ventes.find(v => v.id === id);
    const confirmed = window.confirm(`Êtes-vous sûr de vouloir annuler cette vente (${parseFloat(vente?.montant_total || 0).toFixed(2)} DH) ?`);
    
    if (confirmed) {
      try {
        await annulerVente(id);
        setSuccess('Vente annulée avec succès');
        loadData();
        setTimeout(() => setSuccess(null), 3000);
      } catch (err) {
        setError('Erreur lors de l\'annulation de la vente');
        console.error(err);
      }
    }
  };

  if (loading) {
    return <div className="loading"><div className="spinner"></div></div>;
  }

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
        <h1 className="page-title" style={{ marginBottom: 0 }}>Ventes</h1>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Annuler' : '+ Nouvelle vente'}
        </button>
      </div>

      {error && <div className="alert alert-error">{error}</div>}
      {success && <div className="alert alert-success">{success}</div>}

      {showForm && (
        <div className="card">
          <h2 className="card-title">Nouvelle vente</h2>

          {/* Sélection médicaments */}
          <div className="form-group">
            <label className="form-label">Ajouter un médicament</label>
            <select
              className="form-select"
              onChange={(e) => {
                const med = medicaments.find(m => m.id === parseInt(e.target.value));
                if (med) {
                  addToCart(med);
                  e.target.value = '';
                }
              }}
            >
              <option value="">Sélectionner un médicament...</option>
              {medicaments.filter(m => m.stock_actuel > 0).map(med => (
                <option key={med.id} value={med.id}>
                  {med.nom} ({med.dosage}) - Stock: {med.stock_actuel} - {parseFloat(med.prix_vente).toFixed(2)} DH
                </option>
              ))}
            </select>
          </div>

          {/* Panier */}
          {cart.length > 0 && (
            <div style={{ marginTop: '1.5rem' }}>
              <h3 style={{ marginBottom: '1rem' }}>Panier</h3>
              <table className="table">
                <thead>
                  <tr>
                    <th>Médicament</th>
                    <th>Prix unitaire</th>
                    <th>Quantité</th>
                    <th>Sous-total</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {cart.map(item => (
                    <tr key={item.medicament.id}>
                      <td>{item.medicament.nom} ({item.medicament.dosage})</td>
                      <td>{parseFloat(item.medicament.prix_vente).toFixed(2)} DH</td>
                      <td>
                        <input
                          type="number"
                          min="1"
                          max={item.medicament.stock_actuel}
                          value={item.quantite}
                          onChange={(e) => updateCartQuantity(item.medicament.id, e.target.value)}
                          style={{ width: '80px', padding: '0.25rem' }}
                          className="form-input"
                        />
                      </td>
                      <td>{(parseFloat(item.medicament.prix_vente) * item.quantite).toFixed(2)} DH</td>
                      <td>
                        <button
                          className="btn btn-danger"
                          onClick={() => removeFromCart(item.medicament.id)}
                          style={{ fontSize: '0.75rem', padding: '0.25rem 0.5rem' }}
                        >
                          <FaTimes /> Retirer
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
                <tfoot>
                  <tr>
                    <td colSpan="3" style={{ textAlign: 'right', fontWeight: 'bold' }}>Total:</td>
                    <td colSpan="2" style={{ fontWeight: 'bold', fontSize: '1.25rem', color: '#2563eb' }}>
                      {calculateTotal()} DH
                    </td>
                  </tr>
                </tfoot>
              </table>

              <button className="btn btn-success" onClick={handleSubmitVente}>
                <FaShoppingCart /> Valider la vente
              </button>
            </div>
          )}
        </div>
      )}

      {/* Liste des ventes */}
      <div className="card">
        <h2 className="card-title">Historique des ventes</h2>
        <div style={{ overflowX: 'auto' }}>
          <table className="table">
            <thead>
              <tr>
                <th>Référence</th>
                <th>Date</th>
                <th>Total TTC</th>
                <th>Statut</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {ventes.map(vente => (
                <tr key={vente.id}>
                  <td>{vente.reference}</td>
                  <td>{new Date(vente.date_vente).toLocaleString('fr-FR')}</td>
                  <td>{parseFloat(vente.total_ttc).toFixed(2)} DH</td>
                  <td>
                    <span className={`badge ${
                      vente.statut === 'completee' ? 'badge-success' :
                      vente.statut === 'annulee' ? 'badge-danger' : 'badge-warning'
                    }`}>
                      {vente.statut}
                    </span>
                  </td>
                  <td>
                    {vente.statut === 'completee' && (
                      <button
                        className="btn btn-danger"
                        onClick={() => handleAnnulerVente(vente.id)}
                        style={{ fontSize: '0.75rem', padding: '0.25rem 0.5rem' }}
                      >
                        <FaBan /> Annuler
                      </button>
                    )}
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

export default VentesPage;
