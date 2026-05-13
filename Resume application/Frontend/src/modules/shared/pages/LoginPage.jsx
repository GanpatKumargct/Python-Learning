import React from 'react';

export default function LoginPage() {
  const handleZohoLogin = () => {
    window.location.href = 'http://localhost:8000/api/v1/auth/zoho/login';
  };

  return (
    <div className="bg-gray-900/40 backdrop-blur-xl border border-gray-800 rounded-3xl p-8 shadow-2xl text-center">
      <div className="mb-8">
        <div className="mx-auto w-16 h-16 bg-blue-500/10 flex items-center justify-center rounded-2xl border border-blue-500/20 mb-6 shadow-lg shadow-blue-500/10">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
             <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 11c0 3.517-1.009 6.799-2.753 9.571m-3.44-2.04l.054-.09A13.916 13.916 0 008 11a4 4 0 118 0c0 1.017-.07 2.019-.203 3m-2.118 6.844A21.88 21.88 0 0015.171 17m3.839 1.132c.645-2.266.99-4.659.99-7.132A8 8 0 008 4.07M3 15.364c.64-1.319 1-2.8 1-4.364 0-1.457.39-2.823 1.07-4" />
          </svg>
        </div>
        <h2 className="text-3xl font-extrabold text-white mb-2 tracking-tight">Staff Login</h2>
        <p className="text-gray-400 text-sm max-w-sm mx-auto">
          Access the ERP workspace securely using your corporate Zoho account.
        </p>
      </div>

      <button 
        onClick={handleZohoLogin}
        className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-500 hover:to-purple-500 text-white font-semibold rounded-xl px-4 py-3.5 shadow-lg shadow-blue-500/25 transition-all active:scale-[0.98] flex items-center justify-center gap-3 mt-2"
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
           <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm0 18c-3.314 0-6-2.686-6-6s2.686-6 6-6 6 2.686 6 6-2.686 6-6 6z"/>
        </svg>
        Sign in with Zoho SSO
      </button>
      
      <div className="mt-8 pt-6 border-t border-gray-800/50 text-sm text-gray-500">
        Applying for a role? <br/>
        <a href="/candidate/login" className="text-blue-400 hover:text-blue-300 transition-colors font-medium inline-block mt-1">Go to Candidate Portal</a>
      </div>
    </div>
  );
}
