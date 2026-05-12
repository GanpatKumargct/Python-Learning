import React, { useState, useEffect } from 'react';
import apiClient from '../../../lib/apiClient';

export default function JobRequisitionsPage() {
  const [requisitions, setRequisitions] = useState([]);
  const [forms, setForms] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  // Form State
  const [title, setTitle] = useState('');
  const [department, setDepartment] = useState('');
  const [location, setLocation] = useState('');
  const [description, setDescription] = useState('');
  const [scope, setScope] = useState('');
  const [selectedForm, setSelectedForm] = useState('');
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [reqRes, formsRes] = await Promise.all([
        apiClient.get('/requisitions/'),
        apiClient.get('/forms/')
      ]);
      setRequisitions(reqRes.data);
      setForms(formsRes.data);
      if (formsRes.data.length > 0) {
        setSelectedForm(formsRes.data[0].id);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setCreating(true);
    try {
      await apiClient.post('/requisitions/', {
        title,
        department,
        location,
        job_description: description,
        scope_of_work: scope,
        screening_form_id: selectedForm
      });
      setShowModal(false);
      setTitle(''); setDepartment(''); setLocation(''); setDescription(''); setScope('');
      fetchData();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to create requisition');
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="flex-1 max-w-7xl w-full mx-auto p-8 font-sans animate-fade-in text-white">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h2 className="text-3xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">Job Requisitions</h2>
          <p className="text-gray-400 mt-1">Manage open roles and application pipelines.</p>
        </div>
        <button 
          onClick={() => setShowModal(true)}
          className="bg-blue-600 hover:bg-blue-500 text-white font-medium px-5 py-2.5 rounded-xl shadow-lg shadow-blue-500/20 transition-all flex items-center gap-2"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
          </svg>
          New Requisition
        </button>
      </div>

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        </div>
      ) : requisitions.length === 0 ? (
        <div className="border-2 border-dashed border-gray-800 rounded-3xl p-16 flex flex-col items-center justify-center text-center">
          <h3 className="text-xl font-bold text-gray-300 mb-2">No Job Requisitions</h3>
          <p className="text-gray-500 max-w-sm mb-6">Create your first job requisition to start accepting candidate applications.</p>
          <button onClick={() => setShowModal(true)} className="text-blue-400 font-medium hover:text-blue-300">Create Requisition &rarr;</button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {requisitions.map(req => (
            <div key={req.id} className="bg-gray-900 border border-gray-800 rounded-2xl p-6 hover:border-gray-700 transition-colors group cursor-pointer">
              <div className="flex justify-between items-start mb-4">
                <span className={`px-2.5 py-1 rounded-md text-xs font-bold uppercase tracking-wider ${req.status === 'published' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-amber-500/10 text-amber-400'}`}>
                  {req.status}
                </span>
                <span className="text-xs text-gray-500 font-medium">{new Date(req.created_at).toLocaleDateString()}</span>
              </div>
              <h3 className="text-xl font-bold text-white mb-1 group-hover:text-blue-400 transition-colors">{req.title}</h3>
              <p className="text-sm text-gray-400 mb-4">{req.department} • {req.location || 'Remote'}</p>
              <div className="mt-4 pt-4 border-t border-gray-800 flex justify-between items-center text-sm">
                <span className="text-gray-500">0 Candidates</span>
                <button className="text-blue-500 font-medium hover:text-blue-400 transition-colors">View Pipeline &rarr;</button>
              </div>
            </div>
          ))}
        </div>
      )}

      {showModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 border border-gray-800 rounded-3xl p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto animate-fade-in-up shadow-2xl">
            <h2 className="text-2xl font-bold text-white mb-6">Create New Requisition</h2>
            <form onSubmit={handleCreate} className="space-y-5">
              <div className="grid grid-cols-2 gap-5">
                <div className="space-y-1.5">
                  <label className="text-sm font-medium text-gray-400">Job Title</label>
                  <input required value={title} onChange={e => setTitle(e.target.value)} className="w-full bg-black/50 border border-gray-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500" placeholder="e.g. Senior Backend Engineer" />
                </div>
                <div className="space-y-1.5">
                  <label className="text-sm font-medium text-gray-400">Department</label>
                  <input required value={department} onChange={e => setDepartment(e.target.value)} className="w-full bg-black/50 border border-gray-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500" placeholder="e.g. Engineering" />
                </div>
              </div>
              
              <div className="space-y-1.5">
                <label className="text-sm font-medium text-gray-400">Location</label>
                <input required value={location} onChange={e => setLocation(e.target.value)} className="w-full bg-black/50 border border-gray-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500" placeholder="e.g. Remote / New York" />
              </div>

              <div className="space-y-1.5">
                <label className="text-sm font-medium text-gray-400">Application Form (Dynamic Builder)</label>
                <select 
                  required 
                  value={selectedForm} 
                  onChange={e => setSelectedForm(e.target.value)}
                  className="w-full bg-black/50 border border-gray-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500 appearance-none"
                >
                  <option value="" disabled>Select a form schema</option>
                  {forms.map(form => (
                    <option key={form.id} value={form.id}>{form.title}</option>
                  ))}
                </select>
              </div>

              <div className="space-y-1.5">
                <label className="text-sm font-medium text-gray-400">Job Description</label>
                <textarea required value={description} onChange={e => setDescription(e.target.value)} rows={3} className="w-full bg-black/50 border border-gray-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500 resize-none" placeholder="Describe the role..."></textarea>
              </div>

              <div className="flex gap-4 pt-4 border-t border-gray-800">
                <button type="button" onClick={() => setShowModal(false)} className="flex-1 bg-gray-800 hover:bg-gray-700 text-white font-medium py-3 rounded-xl transition-all">Cancel</button>
                <button type="submit" disabled={creating} className="flex-1 bg-blue-600 hover:bg-blue-500 text-white font-medium py-3 rounded-xl transition-all disabled:opacity-50">
                  {creating ? 'Creating...' : 'Create Draft Requisition'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
