/**
 * API pour la gestion des catégories.
 */
import axiosInstance from './axiosConfig';

/**
 * Récupère toutes les catégories.
 * @returns {Promise<Array>} Liste des catégories
 */
export const fetchCategories = async () => {
    const response = await axiosInstance.get('/categories/');
    return response.data;
};

/**
 * Crée une nouvelle catégorie.
 * @param {Object} data - Données de la catégorie
 * @returns {Promise<Object>} Catégorie créée
 */
export const createCategorie = async (data) => {
    const response = await axiosInstance.post('/categories/', data);
    return response.data;
};

/**
 * Met à jour une catégorie.
 * @param {number} id - ID de la catégorie
 * @param {Object} data - Nouvelles données
 * @returns {Promise<Object>} Catégorie mise à jour
 */
export const updateCategorie = async (id, data) => {
    const response = await axiosInstance.put(`/categories/${id}/`, data);
    return response.data;
};

/**
 * Supprime une catégorie.
 * @param {number} id - ID de la catégorie
 * @returns {Promise<void>}
 */
export const deleteCategorie = async (id) => {
    await axiosInstance.delete(`/categories/${id}/`);
};
