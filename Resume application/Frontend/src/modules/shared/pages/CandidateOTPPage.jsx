import React, { useState } from 'react';
import apiClient from '../../../lib/apiClient';

export default function CandidateOTPPage() {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState('idle'); // 'idle' | 'loading' | 'success' | 'error'
  const [error, setError] = useState('');

  const handleRequestMagicLink = async (e) => {
    e.preventDefault();
    setStatus('loading');
    setError('');

    try {
      await apiClient.post('/auth/candidate/send-magic-link', { email, purpose: 'magic_link' });
      setStatus('success');
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to send login link. Please try again.');
      setStatus('error');
    }
  };

  return (
    <div className="bg-gray-900/40 backdrop-blur-xl border border-gray-800 rounded-3xl p-8 shadow-2xl relative overflow-hidden text-center">
      <div className="mb-8 mt-2">
        <h2 className="text-3xl font-extrabold text-white mb-2 tracking-tight">Candidate Portal</h2>
        <p className="text-gray-400 text-sm max-w-sm mx-auto">
          {status === 'success' 
            ? "Check your email!" 
            : "Enter your email to receive a secure, passwordless magic login link."}
        </p>
      </div>

      {status === 'success' ? (
        <div className="py-6 animate-fade-in">
          <div className="w-16 h-16 bg-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center mx-auto mb-4 border border-emerald-500/30">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
            </svg>
          </div>
          <p className="text-gray-300">We've sent a magic link to <strong className="text-white">{email}</strong>.</p>
          <p className="text-gray-500 text-sm mt-2">Click the link in the email to sign in securely.</p>
          <button 
            onClick={() => setStatus('idle')}
            className="mt-6 text-emerald-400 hover:text-emerald-300 transition-colors text-sm font-medium"
          >
            Didn't receive it? Try again
          </button>
        </div>
      ) : (
        <form onSubmit={handleRequestMagicLink} className="space-y-5">
          {status === 'error' && (
            <div className="p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm font-medium">
              {error}
            </div>
          )}

          <div className="space-y-1.5 animate-fade-in text-left">
            <label className="text-sm font-medium text-gray-300 ml-1">Email Address</label>
            <input 
              type="email" 
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full bg-gray-950/50 border border-gray-800 rounded-xl px-4 py-3 text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/50 focus:border-emerald-500 transition-all text-lg tracking-wide"
              placeholder="applicant@email.com"
            />
          </div>

          <button 
            type="submit" 
            disabled={status === 'loading'}
            className="w-full bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 text-white font-semibold rounded-xl px-4 py-3.5 shadow-lg shadow-emerald-500/25 transition-all active:scale-[0.98] disabled:opacity-50 flex items-center justify-center gap-2 mt-2"
          >
            {status === 'loading' ? (
              <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            ) : 'Send Magic Link'}
          </button>
        </form>
      )}
      
      <div className="mt-8 pt-6 border-t border-gray-800/50 text-sm text-gray-500">
        Internal staff member? <br/>
        <a href="/login" className="text-emerald-400 hover:text-emerald-300 transition-colors font-medium inline-block mt-1">Switch to Staff Login</a>
      </div>
    </div>
  );
}
