import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../api/axios';

const Register = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [fullName, setFullName] = useState('');
    const [error, setError] = useState('');
    const navigate = useNavigate();

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // External user registration
            await api.post('/auth/register', {
                email,
                password,
                full_name: fullName
            });
            navigate('/login');
        } catch (err) {
            setError(err.response?.data?.detail || 'Registration failed');
        }
    };

    return (
        <div className="container">
            <div className="card">
                <h2>Register</h2>
                {error && <div className="error">{error}</div>}
                <form onSubmit={handleSubmit}>
                    <input 
                        type="text" 
                        placeholder="Full Name" 
                        value={fullName} 
                        onChange={(e) => setFullName(e.target.value)} 
                    />
                    <input 
                        type="email" 
                        placeholder="Email" 
                        value={email} 
                        onChange={(e) => setEmail(e.target.value)} 
                        required 
                    />
                    <input 
                        type="password" 
                        placeholder="Password" 
                        value={password} 
                        onChange={(e) => setPassword(e.target.value)} 
                        required 
                    />
                    <button type="submit">Register</button>
                </form>
            </div>
        </div>
    );
};

export default Register;
