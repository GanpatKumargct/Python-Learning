import React, { useEffect, useState } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../../store/authStore';
import apiClient from '../../../lib/apiClient';

export default function VerifyMagicLinkPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const setAuth = useAuthStore((state) => state.setAuth);
  const [status, setStatus] = useState('verifying'); // verifying | error

  useEffect(() => {
    const verifyToken = async () => {
      const token = searchParams.get('token');
      const email = searchParams.get('email');

      if (!token || !email) {
        setStatus('error');
        return;
      }

      try {
        const response = await apiClient.post('/auth/candidate/verify-magic-link', { 
          email, 
          token, 
          purpose: 'magic_link' 
        });
        
        const user = { email, role: 'candidate' };
        setAuth(user, response.data.access_token);
        navigate('/candidate/portal');
      } catch (err) {
        setStatus('error');
      }
    };

    verifyToken();
  }, [searchParams, navigate, setAuth]);

  if (status === 'error') {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-[#0A0A0A] text-white p-4">
        <div className="w-16 h-16 bg-red-500/10 text-red-500 flex items-center justify-center rounded-2xl mb-4 border border-red-500/20">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </div>
        <h2 className="text-2xl font-bold mb-2">Invalid or Expired Link</h2>
        <p className="text-gray-400 mb-6 text-center max-w-md">The magic link you clicked is either invalid or has expired. Please request a new one.</p>
        <button 
          onClick={() => navigate('/candidate/login')}
          className="bg-gray-800 hover:bg-gray-700 text-white px-6 py-2.5 rounded-lg transition-colors"
        >
          Request New Link
        </button>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#0A0A0A] text-white">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-500 mb-4"></div>
      <h2 className="text-xl font-medium text-gray-300">Verifying your secure link...</h2>
    </div>
  );
}
