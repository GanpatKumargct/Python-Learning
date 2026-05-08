import React, { useState } from 'react';
import { Plus, Check, X, Search } from 'lucide-react';
import { jobs as initialJobs, applications } from '../data/mockData';

const JobManagement = () => {
  const [jobs, setJobs] = useState(initialJobs);
  const [showForm, setShowForm] = useState(false);
  const [newJob, setNewJob] = useState({ title: '', description: '', location: '', openings_count: 1 });

  const getAppCount = (jobId) => {
    return applications.filter(app => app.job_id === jobId).length;
  };

  const handleToggleStatus = (id) => {
    setJobs(jobs.map(job => 
      job.id === id ? { ...job, is_active: !job.is_active } : job
    ));
  };

  const handleCreateJob = (e) => {
    e.preventDefault();
    const job = {
      id: Math.random().toString(36).substr(2, 9),
      ...newJob,
      is_active: true
    };
    setJobs([job, ...jobs]);
    setShowForm(false);
    setNewJob({ title: '', description: '', location: '', openings_count: 1 });
  };

  return (
    <div className="animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold text-slate-800">Job Postings</h1>
          <p className="text-slate-500">Manage your open roles and view applicant counts.</p>
        </div>
        <button 
          onClick={() => setShowForm(!showForm)}
          className="bg-brand-600 text-white px-5 py-2.5 rounded-xl font-medium flex items-center gap-2 hover:bg-brand-700 hover:shadow-lg hover:shadow-brand-500/20 transition-all active:scale-95"
        >
          {showForm ? <X size={18} /> : <Plus size={18} />}
          {showForm ? 'Cancel' : 'Create New Job'}
        </button>
      </div>

      {showForm && (
        <div className="bg-white p-6 rounded-2xl shadow-sm border border-brand-100 mb-8 animate-in slide-in-from-top-4 duration-300">
          <h2 className="text-xl font-bold text-slate-800 mb-6">Post a New Role</h2>
          <form onSubmit={handleCreateJob} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Job Title</label>
                <input 
                  type="text" 
                  required
                  value={newJob.title}
                  onChange={e => setNewJob({...newJob, title: e.target.value})}
                  className="w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none"
                  placeholder="e.g. Product Manager"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Location</label>
                <input 
                  type="text" 
                  required
                  value={newJob.location}
                  onChange={e => setNewJob({...newJob, location: e.target.value})}
                  className="w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none"
                  placeholder="e.g. Remote, USA"
                />
              </div>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Description</label>
              <textarea 
                required
                value={newJob.description}
                onChange={e => setNewJob({...newJob, description: e.target.value})}
                className="w-full px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none"
                rows="3"
                placeholder="Briefly describe the role..."
              ></textarea>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Total Openings</label>
              <input 
                type="number" 
                min="1"
                required
                value={newJob.openings_count}
                onChange={e => setNewJob({...newJob, openings_count: parseInt(e.target.value)})}
                className="w-32 px-4 py-2.5 rounded-lg border border-slate-300 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none"
              />
            </div>

            <div className="pt-2">
              <button type="submit" className="bg-slate-900 text-white px-6 py-2.5 rounded-lg font-medium hover:bg-slate-800 transition-colors">
                Publish Job
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="p-4 border-b border-slate-100 flex items-center gap-2 text-slate-400 bg-slate-50/50">
          <Search size={18} />
          <input 
            type="text" 
            placeholder="Search jobs..." 
            className="bg-transparent border-none outline-none text-sm w-full placeholder:text-slate-400 text-slate-700"
          />
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 text-slate-500 text-xs uppercase tracking-wider">
                <th className="p-4 font-bold">Role Details</th>
                <th className="p-4 font-bold text-center">Openings</th>
                <th className="p-4 font-bold text-center">Applicants</th>
                <th className="p-4 font-bold text-center">Status</th>
                <th className="p-4 font-bold text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-sm">
              {jobs.map(job => (
                <tr key={job.id} className="hover:bg-slate-50/50 transition-colors group">
                  <td className="p-4">
                    <p className="font-bold text-slate-800">{job.title}</p>
                    <p className="text-slate-500 text-xs mt-1">{job.location}</p>
                  </td>
                  <td className="p-4 text-center text-slate-600 font-medium">
                    {job.openings_count}
                  </td>
                  <td className="p-4 text-center">
                    <span className="bg-brand-50 text-brand-700 font-bold px-3 py-1 rounded-full text-xs">
                      {getAppCount(job.id)} Total
                    </span>
                  </td>
                  <td className="p-4 text-center">
                    {job.is_active ? (
                      <span className="inline-flex items-center gap-1.5 text-green-600 bg-green-50 px-2.5 py-1 rounded-md text-xs font-bold">
                        <span className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></span>
                        Open
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1.5 text-slate-500 bg-slate-100 px-2.5 py-1 rounded-md text-xs font-bold">
                        <span className="w-1.5 h-1.5 bg-slate-400 rounded-full"></span>
                        Closed
                      </span>
                    )}
                  </td>
                  <td className="p-4 text-right">
                    <button 
                      onClick={() => handleToggleStatus(job.id)}
                      className={`text-xs font-semibold px-3 py-1.5 rounded-lg transition-colors ${
                        job.is_active 
                          ? 'text-red-600 hover:bg-red-50' 
                          : 'text-green-600 hover:bg-green-50'
                      }`}
                    >
                      {job.is_active ? 'Close Job' : 'Reopen Job'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default JobManagement;
