import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

const Dashboard = () => {
    const { user } = useContext(AuthContext);

    return (
        <div className="container">
            <div className="card">
                <h2>Dashboard</h2>
                <p>Welcome, {user.full_name || user.email}!</p>
                <p>Your Role: <strong>{user.role ? user.role.name : 'External User'}</strong></p>
                <div style={{ marginTop: '1rem', padding: '1rem', background: '#f8fafc', borderRadius: '4px' }}>
                    <h3>Profile Information</h3>
                    <p>Email: {user.email}</p>
                    <p>Account Created: {new Date(user.created_at).toLocaleDateString()}</p>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
