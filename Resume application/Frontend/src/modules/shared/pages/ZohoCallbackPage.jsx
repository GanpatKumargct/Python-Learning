import React, { useEffect } from 'react';
import { useSearchParams, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../../store/authStore';

export default function ZohoCallbackPage() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const setAuth = useAuthStore((state) => state.setAuth);

  useEffect(() => {
    const token = searchParams.get('token');
    
    if (token) {
      // In a real app we'd decode the JWT to get role/email.
      // For now we simulate an admin login
      const user = { email: 'staff@zoho.com', role: 'admin' };
      setAuth(user, token);
      navigate('/app/dashboard');
    } else {
      navigate('/login');
    }
  }, [searchParams, navigate, setAuth]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-[#0A0A0A] text-white">
      <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"></div>
      <h2 className="text-xl font-medium text-gray-300">Authenticating with Zoho SSO...</h2>
    </div>
  );
}
