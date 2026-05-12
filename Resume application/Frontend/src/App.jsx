import React from 'react';
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import AuthLayout from './modules/shared/layouts/AuthLayout';
import LoginPage from './modules/shared/pages/LoginPage';
import CandidateOTPPage from './modules/shared/pages/CandidateOTPPage';
import FormBuilderPage from './modules/forms/pages/FormBuilderPage';
import JobRequisitionsPage from './modules/ats/pages/JobRequisitionsPage';
import UserManagementPage from './modules/admin/pages/UserManagementPage';
import { useAuthStore } from './store/authStore';

// Simple Auth Guard for the Dashboard
function RequireAuth({ children, requireRole }) {
  const token = useAuthStore((state) => state.accessToken);
  const user = useAuthStore((state) => state.user);
  
  if (!token) return <Navigate to="/login" replace />;
  if (requireRole && user?.role !== requireRole && user?.role !== 'admin') {
    return <Navigate to="/app/dashboard" replace />;
  }
  return children;
}

// Temporary Dashboard Component to show successful login
function Dashboard() {
  const user = useAuthStore((state) => state.user);
  const logout = useAuthStore((state) => state.logout);
  const navigate = useNavigate();
  
  return (
    <div className="min-h-screen bg-[#0A0A0A] text-white flex flex-col font-sans">
      <header className="px-8 py-6 border-b border-gray-800 flex justify-between items-center backdrop-blur-md bg-black/50 sticky top-0 z-50">
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => navigate('/app/dashboard')}>
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
          </div>
          <h1 className="text-2xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">Aerospace ERP</h1>
        </div>
        <nav className="flex items-center gap-6 text-sm font-medium">
          <button onClick={() => navigate('/app/requisitions')} className="text-gray-300 hover:text-white transition-colors">Jobs</button>
          <button onClick={() => navigate('/app/forms/builder')} className="text-gray-300 hover:text-white transition-colors">Form Builder</button>
          
          {(user?.role === 'admin' || user?.role === 'hr') && (
            <button onClick={() => navigate('/app/admin/users')} className="text-blue-400 hover:text-blue-300 transition-colors bg-blue-500/10 px-3 py-1.5 rounded-lg border border-blue-500/20">Admin Panel</button>
          )}

          <span className="text-gray-400">Logged in as <span className="text-white">{user?.email}</span> ({user?.role})</span>
          <button onClick={() => logout()} className="px-5 py-2.5 rounded-full bg-red-500/10 hover:bg-red-500/20 transition-all active:scale-95 text-red-500 font-medium backdrop-blur-md border border-red-500/20">
            Logout
          </button>
        </nav>
      </header>

      <main className="flex-1 max-w-7xl w-full mx-auto p-8 flex flex-col gap-8">
        <Routes>
          <Route path="/" element={
            <section className="mt-12 mb-8 animate-fade-in-up">
              <h2 className="text-5xl font-extrabold tracking-tight mb-4 text-transparent bg-clip-text bg-gradient-to-r from-gray-100 to-gray-500">Welcome back.</h2>
              <p className="text-lg text-gray-400 max-w-2xl leading-relaxed">
                You have successfully authenticated via JWT. This is a protected route.
              </p>
            </section>
          } />
          <Route path="/forms/builder" element={<FormBuilderPage />} />
          <Route path="/requisitions" element={<JobRequisitionsPage />} />
          <Route path="/admin/users" element={<UserManagementPage />} />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AuthLayout />}>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/candidate/login" element={<CandidateOTPPage />} />
        </Route>
        
        {/* Protected Dashboard Routes nested */}
        <Route path="/app/*" element={<RequireAuth><Dashboard /></RequireAuth>} />
        <Route path="/candidate/portal" element={<RequireAuth><Dashboard /></RequireAuth>} />
        
        {/* Redirect root to login */}
        <Route path="/" element={<Navigate to="/login" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
