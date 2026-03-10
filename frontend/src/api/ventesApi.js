/**
 * API pour la gestion des ventes.
 */
import axiosInstance from './axiosConfig';

/**
 * Récupère l'historique des ventes.
 * @param {Object} params - Paramètres de filtrage (date_debut, date_fin, statut)
 * @returns {Promise<Object>} Données paginées des ventes
 */
export const fetchVentes = async (params = {}) => {
    const response = await axiosInstance.get('/ventes/', { params });
    return response.data;
};

/**
 * Récupère les détails d'une vente.
 * @param {number} id - ID de la vente
 * @returns {Promise<Object>} Détails de la vente
 */
export const fetchVente = async (id) => {
    const response = await axiosInstance.get(`/ventes/${id}/`);
    return response.data;
};

/**
 * Crée une nouvelle vente.
 * @param {Object} data - Données de la vente avec lignes
 * @returns {Promise<Object>} Vente créée
 */
export const createVente = async (data) => {
    const response = await axiosInstance.post('/ventes/', data);
    return response.data;
};

/**
 * Annule une vente.
 * @param {number} id - ID de la vente
 * @returns {Promise<Object>} Vente annulée
 */
export const annulerVente = async (id) => {
    const response = await axiosInstance.post(`/ventes/${id}/annuler/`);
    return response.data;
};
