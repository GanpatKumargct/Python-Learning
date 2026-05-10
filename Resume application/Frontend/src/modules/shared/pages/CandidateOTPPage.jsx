import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../../store/authStore';
import apiClient from '../../../lib/apiClient';

export default function CandidateOTPPage() {
  const [email, setEmail] = useState('');
  const [otp, setOtp] = useState('');
  const [step, setStep] = useState('email'); // 'email' | 'otp'
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const setAuth = useAuthStore((state) => state.setAuth);
  const navigate = useNavigate();

  const handleRequestOTP = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      await apiClient.post('/auth/candidate/send-otp', { email, purpose: 'magic_link' });
      setStep('otp');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to send OTP. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyOTP = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await apiClient.post('/auth/candidate/verify-otp', { email, otp, purpose: 'magic_link' });
      
      const user = { email, role: 'candidate' }; 
      setAuth(user, response.data.access_token);
      
      // Navigate to candidate dashboard/portal
      navigate('/candidate/portal');
    } catch (err) {
      setError(err.response?.data?.detail || 'Invalid or expired OTP.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-gray-900/40 backdrop-blur-xl border border-gray-800 rounded-3xl p-8 shadow-2xl relative overflow-hidden">
      {step === 'otp' && (
        <button 
          onClick={() => setStep('email')}
          className="absolute top-6 left-6 text-gray-500 hover:text-gray-300 transition-colors"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd" />
          </svg>
        </button>
      )}

      <div className="mb-8 text-center mt-2">
        <h2 className="text-2xl font-bold text-white mb-2">Candidate Portal</h2>
        <p className="text-gray-400 text-sm">
          {step === 'email' 
            ? "Enter your email to receive a magic login code." 
            : "Enter the 6-digit code sent to your email."}
        </p>
      </div>

      <form onSubmit={step === 'email' ? handleRequestOTP : handleVerifyOTP} className="space-y-5">
        {error && (
          <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm font-medium text-center">
            {error}
          </div>
        )}

        {step === 'email' ? (
          <div className="space-y-1.5 animate-fade-in">
            <input 
              type="email" 
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-gray-950/50 border border-gray-800 rounded-xl px-4 py-3.5 text-center text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition-all text-lg tracking-wide"
              placeholder="applicant@email.com"
            />
          </div>
        ) : (
          <div className="space-y-1.5 animate-fade-in">
            <input 
              type="text" 
              required
              maxLength={6}
              value={otp}
              onChange={(e) => setOtp(e.target.value.replace(/\D/g, ''))}
              className="w-full bg-gray-950/50 border border-gray-800 rounded-xl px-4 py-3.5 text-center text-white placeholder-gray-600 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition-all text-2xl tracking-[0.5em] font-mono"
              placeholder="000000"
            />
          </div>
        )}

        <button 
          type="submit" 
          disabled={loading || (step === 'otp' && otp.length < 6)}
          className="w-full bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 text-white font-semibold rounded-xl px-4 py-3.5 shadow-lg shadow-emerald-500/25 transition-all active:scale-[0.98] disabled:opacity-50 flex items-center justify-center gap-2 mt-2"
        >
          {loading ? (
            <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          ) : step === 'email' ? 'Send Magic Code' : 'Verify & Sign In'}
        </button>
      </form>
      
      <div className="mt-8 pt-6 border-t border-gray-800/50 text-center text-sm text-gray-500">
        Internal staff member? <br/>
        <a href="/login" className="text-emerald-400 hover:text-emerald-300 transition-colors font-medium">Switch to Staff Login</a>
      </div>
    </div>
  );
}
