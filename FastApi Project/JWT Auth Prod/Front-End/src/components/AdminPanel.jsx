import React, { useState, useEffect } from 'react';
import api from '../api/axios';

const AdminPanel = () => {
    const [roles, setRoles] = useState([]);
    const [users, setUsers] = useState([]);
    const [newRoleName, setNewRoleName] = useState('');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    useEffect(() => {
        fetchRoles();
        fetchUsers();
    }, []);

    const fetchRoles = async () => {
        try {
            const res = await api.get('/roles/');
            setRoles(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    const fetchUsers = async () => {
        try {
            const res = await api.get('/users/');
            setUsers(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    const handleCreateRole = async (e) => {
        e.preventDefault();
        try {
            await api.post('/roles/', { name: newRoleName, description: 'Created by Admin' });
            setNewRoleName('');
            setSuccess('Role created successfully');
            setError('');
            fetchRoles();
        } catch (err) {
            setError(err.response?.data?.detail || 'Failed to create role');
            setSuccess('');
        }
    };

    const handleAssignRole = async (userId, roleId) => {
        try {
            await api.put(`/users/${userId}/role`, { role_id: roleId });
            setSuccess('Role assigned successfully');
            setError('');
            fetchUsers();
        } catch (err) {
            setError('Failed to assign role');
            setSuccess('');
        }
    };

    return (
        <div className="container">
            <h2>Admin Panel</h2>
            {error && <div className="error">{error}</div>}
            {success && <div style={{ color: 'green', marginBottom: '1rem' }}>{success}</div>}
            
            <div className="card">
                <h3>Create New Role</h3>
                <form onSubmit={handleCreateRole} style={{ display: 'flex', gap: '1rem' }}>
                    <input 
                        type="text" 
                        placeholder="e.g. HR, Process eng, Manager" 
                        value={newRoleName} 
                        onChange={(e) => setNewRoleName(e.target.value)} 
                        required 
                        style={{ marginBottom: 0 }}
                    />
                    <button type="submit">Create Role</button>
                </form>
            </div>

            <div className="card">
                <h3>All Users & Role Assignment</h3>
                <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }}>
                    <thead>
                        <tr style={{ borderBottom: '1px solid #ddd' }}>
                            <th>ID</th>
                            <th>Email</th>
                            <th>Current Role</th>
                            <th>Assign Role</th>
                        </tr>
                    </thead>
                    <tbody>
                        {users.map(u => (
                            <tr key={u.id} style={{ borderBottom: '1px solid #eee' }}>
                                <td style={{ padding: '0.5rem 0' }}>{u.id}</td>
                                <td>{u.email}</td>
                                <td>{u.role ? u.role.name : 'External'}</td>
                                <td>
                                    <select 
                                        onChange={(e) => handleAssignRole(u.id, parseInt(e.target.value))}
                                        defaultValue={u.role_id || ''}
                                        style={{ padding: '0.25rem' }}
                                    >
                                        <option value="" disabled>Select Role</option>
                                        {roles.map(r => (
                                            <option key={r.id} value={r.id}>{r.name}</option>
                                        ))}
                                    </select>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default AdminPanel;
