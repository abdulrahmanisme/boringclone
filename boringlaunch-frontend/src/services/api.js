import axios from 'axios';
import toast from 'react-hot-toast';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add response interceptor for error handling
api.interceptors.response.use(
    (response) => response,
    (error) => {
        const message = error.response?.data?.detail || 'An error occurred';
        toast.error(message);
        return Promise.reject(error);
    }
);

export const startupApi = {
    createStartup: async (data) => {
        const response = await api.post('/startups', data);
        return response.data;
    },

    getAll: async () => {
        const response = await api.get('/startups');
        return response.data;
    },

    get: async (id) => {
        const response = await api.get(`/startups/${id}`);
        return response.data;
    },

    update: async (id, data) => {
        const response = await api.put(`/startups/${id}`, data);
        return response.data;
    },

    delete: async (id) => {
        const response = await api.delete(`/startups/${id}`);
        return response.data;
    },

    uploadLogo: async (id, file) => {
        const formData = new FormData();
        formData.append('file', file);
        const response = await api.post(`/startups/${id}/logo`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },
};

export const platformApi = {
    uploadExcel: async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        const response = await api.post('/platforms/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    getAll: async () => {
        const response = await api.get('/platforms');
        return response.data;
    },

    get: async (id) => {
        const response = await api.get(`/platforms/${id}`);
        return response.data;
    },

    toggle: async (id) => {
        const response = await api.patch(`/platforms/${id}/toggle`);
        return response.data;
    },
};

export const submissionApi = {
    getAll: async () => {
        const response = await api.get('/submissions');
        return response.data;
    },

    get: async (id) => {
        const response = await api.get(`/submissions/${id}`);
        return response.data;
    },

    create: async (data) => {
        const response = await api.post('/submissions', data);
        return response.data;
    },

    updateStatus: async (id, status, errorMessage = null) => {
        const response = await api.patch(`/submissions/${id}/status`, {
            status,
            error_message: errorMessage,
        });
        return response.data;
    },

    getByStartup: async (startupId) => {
        const response = await api.get(`/submissions/startup/${startupId}`);
        return response.data;
    },
}; 