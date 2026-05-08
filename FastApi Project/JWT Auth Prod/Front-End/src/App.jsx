import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Link } from 'react-router-dom';
import { AuthContext } from './context/AuthContext';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import AdminPanel from './components/AdminPanel';

// Protected Route component checks if user exists
const ProtectedRoute = ({ children, requiredRole }) => {
    const { user, loading } = useContext(AuthContext);

    if (loading) return <div>Loading...</div>;
    
    if (!user) {
        return <Navigate to="/login" />;
    }

    // RBAC check on Frontend
    if (requiredRole && (!user.role || user.role.name !== requiredRole)) {
        return <div className="container"><h2>Access Denied</h2><p>You do not have the required role.</p></div>;
    }

    return children;
};

const App = () => {
    const { user, logout, loading } = useContext(AuthContext);

    if (loading) return <div>Loading Application...</div>;

    return (
        <Router>
            <div style={{ padding: '1rem', background: '#fff', borderBottom: '1px solid #ddd', marginBottom: '2rem' }}>
                <nav style={{ display: 'flex', gap: '1rem', maxWidth: '800px', margin: '0 auto' }}>
                    <Link to="/">Home</Link>
                    {!user ? (
                        <>
                            <Link to="/login">Login</Link>
                            <Link to="/register">Register</Link>
                        </>
                    ) : (
                        <>
                            <Link to="/dashboard">Dashboard</Link>
                            {user.role && user.role.name === 'Admin' && (
                                <Link to="/admin">Admin Panel</Link>
                            )}
                            <button onClick={logout} style={{ marginLeft: 'auto' }}>Logout</button>
                        </>
                    )}
                </nav>
            </div>

            <Routes>
                <Route path="/" element={<div className="container"><h1>Welcome to JWT Auth Demo</h1><p>Production level RBAC example.</p></div>} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                
                {/* Standard Protected Route */}
                <Route path="/dashboard" element={
                    <ProtectedRoute>
                        <Dashboard />
                    </ProtectedRoute>
                } />

                {/* Admin Only Route */}
                <Route path="/admin" element={
                    <ProtectedRoute requiredRole="Admin">
                        <AdminPanel />
                    </ProtectedRoute>
                } />
            </Routes>
        </Router>
    );
};

export default App;
