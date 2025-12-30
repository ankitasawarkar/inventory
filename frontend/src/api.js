import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth
export const login = (username, password) =>
  api.post('/api/auth/login', new URLSearchParams({ username, password }), {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });

// Products
export const getProducts = (params) => api.get('/api/products', { params });
export const getProduct = (id) => api.get(`/api/products/${id}`);
export const createProduct = (data) => api.post('/api/products', data);
export const updateProduct = (id, data) => api.put(`/api/products/${id}`, data);
export const replicateProduct = (id, copyImages = false) =>
  api.post(`/api/products/${id}/replicate?copy_images=${copyImages}`);

// Categories
export const getCategories = () => api.get('/api/categories');
export const createCategory = (data) => api.post('/api/categories', data);

// Cart
export const getCart = (cartId) => api.get(`/api/cart/${cartId}`);
export const addToCart = (cartId, data) => api.post(`/api/cart/${cartId}/items`, data);
export const removeFromCart = (cartId, itemId) =>
  api.delete(`/api/cart/${cartId}/items/${itemId}`);

// Orders
export const getOrders = () => api.get('/api/orders');
export const getOrder = (id) => api.get(`/api/orders/${id}`);
export const createOrder = (data, cartId) =>
  api.post(`/api/orders${cartId ? `?cart_id=${cartId}` : ''}`, data);

// Inventory
export const getInventory = () => api.get('/api/inventory');
export const adjustInventory = (id, data) =>
  api.patch(`/api/inventory/${id}/adjust`, data);

// Reports
export const getProductionReport = (params) =>
  api.get('/api/reports/production', { params });
export const getProfitReport = (params) => api.get('/api/reports/profit', { params });
export const getPipeline = () => api.get('/api/reports/pipeline');

export default api;
