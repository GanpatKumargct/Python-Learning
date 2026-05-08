import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Outlet } from 'react-router-dom';
import { Briefcase, LayoutDashboard, Settings } from 'lucide-react';
import JobListing from './pages/JobListing';
import ApplicationForm from './pages/ApplicationForm';
import PipelineBoard from './pages/PipelineBoard';
import JobManagement from './pages/JobManagement';

// Layout for the public-facing Candidate side
const CandidateLayout = () => {
  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-5xl mx-auto px-4 py-4 flex justify-between items-center">
          <div className="flex items-center gap-2">
            <div className="bg-brand-500 text-white p-2 rounded-lg">
              <Briefcase size={24} />
            </div>
            <h1 className="text-xl font-bold text-slate-800 tracking-tight">Mini-ATS</h1>
          </div>
          <Link to="/admin" className="text-sm font-medium text-slate-500 hover:text-brand-600 transition-colors">
            HR Login
          </Link>
        </div>
      </header>
      <main className="max-w-5xl mx-auto px-4 py-8">
        <Outlet />
      </main>
    </div>
  );
};

// Layout for the internal HR/Recruiter Dashboard
const AdminLayout = () => {
  return (
    <div className="min-h-screen bg-slate-100 flex">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-200 flex flex-col">
        <div className="p-6 border-b border-slate-200 flex items-center gap-3">
          <div className="bg-slate-800 text-white p-2 rounded-lg shadow-md">
            <LayoutDashboard size={20} />
          </div>
          <h2 className="text-lg font-bold text-slate-800">HR Dashboard</h2>
        </div>
        <nav className="p-4 flex-1 flex flex-col gap-2">
          <Link to="/admin" className="flex items-center gap-3 px-4 py-3 rounded-xl text-slate-600 hover:bg-brand-50 hover:text-brand-600 font-medium transition-all">
            <LayoutDashboard size={18} />
            Pipeline
          </Link>
          <Link to="/admin/jobs" className="flex items-center gap-3 px-4 py-3 rounded-xl text-slate-600 hover:bg-brand-50 hover:text-brand-600 font-medium transition-all">
            <Briefcase size={18} />
            Jobs
          </Link>
        </nav>
        <div className="p-4 border-t border-slate-200">
          <Link to="/" className="flex items-center gap-3 px-4 py-3 rounded-xl text-slate-500 hover:bg-slate-100 font-medium transition-all">
            <Settings size={18} />
            Public Site
          </Link>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 overflow-x-hidden overflow-y-auto">
        <div className="p-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<CandidateLayout />}>
          <Route index element={<JobListing />} />
          <Route path="apply/:jobId" element={<ApplicationForm />} />
        </Route>

        {/* HR Admin Routes */}
        <Route path="/admin" element={<AdminLayout />}>
          <Route index element={<PipelineBoard />} />
          <Route path="jobs" element={<JobManagement />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
