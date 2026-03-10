/**
 * API pour la gestion des médicaments.
 */
import axiosInstance from './axiosConfig';

/**
 * Récupère la liste paginée des médicaments.
 * @param {Object} params - Paramètres de filtrage (search, categorie, page)
 * @returns {Promise<Object>} Données paginées des médicaments
 */
export const fetchMedicaments = async (params = {}) => {
    const response = await axiosInstance.get('/medicaments/', { params });
    return response.data;
};

/**
 * Récupère les détails d'un médicament.
 * @param {number} id - ID du médicament
 * @returns {Promise<Object>} Détails du médicament
 */
export const fetchMedicament = async (id) => {
    const response = await axiosInstance.get(`/medicaments/${id}/`);
    return response.data;
};

/**
 * Crée un nouveau médicament.
 * @param {Object} data - Données du médicament
 * @returns {Promise<Object>} Médicament créé
 */
export const createMedicament = async (data) => {
    const response = await axiosInstance.post('/medicaments/', data);
    return response.data;
};

/**
 * Met à jour un médicament.
 * @param {number} id - ID du médicament
 * @param {Object} data - Nouvelles données
 * @returns {Promise<Object>} Médicament mis à jour
 */
export const updateMedicament = async (id, data) => {
    const response = await axiosInstance.put(`/medicaments/${id}/`, data);
    return response.data;
};

/**
 * Supprime un médicament (soft delete).
 * @param {number} id - ID du médicament
 * @returns {Promise<void>}
 */
export const deleteMedicament = async (id) => {
    await axiosInstance.delete(`/medicaments/${id}/`);
};

/**
 * Récupère les médicaments en alerte de stock.
 * @returns {Promise<Array>} Liste des médicaments en alerte
 */
export const fetchMedicamentsAlertes = async () => {
    const response = await axiosInstance.get('/medicaments/alertes/');
    return response.data;
};
