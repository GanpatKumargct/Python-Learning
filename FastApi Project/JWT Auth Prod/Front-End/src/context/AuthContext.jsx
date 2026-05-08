import React, { createContext, useState, useEffect } from 'react';
import api from '../api/axios';

// Create the authentication context for global state
export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        // On initial load, check if user is logged in
        checkUserStatus();
    }, []);

    const checkUserStatus = async () => {
        const token = localStorage.getItem('token');
        if (token) {
            try {
                // Set token for api calls
                api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
                // Fetch current user details to get roles
                const res = await api.get('/users/me');
                setUser(res.data);
            } catch (err) {
                console.error("Invalid token", err);
                localStorage.removeItem('token');
                delete api.defaults.headers.common['Authorization'];
            }
        }
        setLoading(false);
    };

    const login = async (email, password) => {
        const formData = new FormData();
        formData.append('username', email); // OAuth2 expects 'username'
        formData.append('password', password);
        
        const res = await api.post('/auth/login', formData);
        const token = res.data.access_token;
        
        localStorage.setItem('token', token);
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        
        const userRes = await api.get('/users/me');
        setUser(userRes.data);
    };

    const logout = () => {
        localStorage.removeItem('token');
        delete api.defaults.headers.common['Authorization'];
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};
