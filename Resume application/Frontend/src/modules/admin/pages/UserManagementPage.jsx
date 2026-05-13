import React, { useState, useEffect } from 'react';
import apiClient from '../../../lib/apiClient';

export default function UserManagementPage() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  // Form State
  const [email, setEmail] = useState('');
  const [fullName, setFullName] = useState('');
  const [role, setRole] = useState('ptc');
  const [department, setDepartment] = useState('');
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const res = await apiClient.get('/admin/users');
      setUsers(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    setCreating(true);
    try {
      await apiClient.post('/admin/users', {
        email,
        full_name: fullName,
        role,
        department
      });
      setShowModal(false);
      setEmail(''); setFullName(''); setRole(''); setDepartment('');
      fetchUsers();
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to create user');
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="flex-1 max-w-7xl w-full mx-auto p-8 font-sans animate-fade-in text-white">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h2 className="text-3xl font-extrabold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">User Management</h2>
          <p className="text-gray-400 mt-1">Manage staff, assign roles, and control access levels.</p>
        </div>
        <button 
          onClick={() => setShowModal(true)}
          className="bg-blue-600 hover:bg-blue-500 text-white font-medium px-5 py-2.5 rounded-xl shadow-lg shadow-blue-500/20 transition-all flex items-center gap-2"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd" />
          </svg>
          Add Employee
        </button>
      </div>

      <div className="bg-gray-900 border border-gray-800 rounded-3xl overflow-hidden shadow-2xl">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-gray-950/50 border-b border-gray-800 text-xs uppercase tracking-wider text-gray-500 font-bold">
                <th className="p-5 font-bold">Employee</th>
                <th className="p-5 font-bold">Role</th>
                <th className="p-5 font-bold">Department</th>
                <th className="p-5 font-bold">Status</th>
                <th className="p-5 font-bold text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-800">
              {loading ? (
                <tr><td colSpan="5" className="p-8 text-center text-gray-500">Loading users...</td></tr>
              ) : users.length === 0 ? (
                <tr><td colSpan="5" className="p-8 text-center text-gray-500">No users found.</td></tr>
              ) : (
                users.map(user => (
                  <tr key={user.id} className="hover:bg-gray-800/50 transition-colors">
                    <td className="p-5">
                      <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center text-white font-bold text-sm shadow-inner">
                          {user.full_name.charAt(0)}
                        </div>
                        <div>
                          <p className="font-semibold text-white">{user.full_name}</p>
                          <p className="text-xs text-gray-500">{user.email}</p>
                        </div>
                      </div>
                    </td>
                    <td className="p-5">
                      <span className="px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider bg-blue-500/10 text-blue-400 border border-blue-500/20">
                        {user.role.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="p-5 text-gray-400 text-sm">{user.department || '—'}</td>
                    <td className="p-5">
                      <div className="flex items-center gap-2">
                        <div className={`w-2 h-2 rounded-full ${user.is_active ? 'bg-emerald-500' : 'bg-red-500'}`}></div>
                        <span className="text-sm text-gray-300">{user.is_active ? 'Active' : 'Disabled'}</span>
                      </div>
                    </td>
                    <td className="p-5 text-right">
                      <button className="text-gray-400 hover:text-white transition-colors p-2 hover:bg-gray-800 rounded-lg">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                        </svg>
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <div className="bg-gray-900 border border-gray-800 rounded-3xl p-8 max-w-xl w-full max-h-[90vh] overflow-y-auto animate-fade-in-up shadow-2xl">
            <h2 className="text-2xl font-bold text-white mb-6">Add New Employee</h2>
            <form onSubmit={handleCreateUser} className="space-y-5">
              <div className="grid grid-cols-2 gap-5">
                <div className="space-y-1.5">
                  <label className="text-sm font-medium text-gray-400">Full Name</label>
                  <input required value={fullName} onChange={e => setFullName(e.target.value)} className="w-full bg-black/50 border border-gray-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500" placeholder="Jane Doe" />
                </div>
                <div className="space-y-1.5">
                  <label className="text-sm font-medium text-gray-400">Email Address</label>
                  <input type="email" required value={email} onChange={e => setEmail(e.target.value)} className="w-full bg-black/50 border border-gray-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500" placeholder="jane@aerospace.com" />
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-5">
                <div className="space-y-1.5">
                  <label className="text-sm font-medium text-gray-400">System Role</label>
                  <input 
                    required 
                    value={role} 
                    onChange={e => setRole(e.target.value)}
                    className="w-full bg-black/50 border border-gray-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500"
                    placeholder="e.g. Hiring Manager"
                  />
                </div>
                <div className="space-y-1.5">
                  <label className="text-sm font-medium text-gray-400">Department</label>
                  <input required value={department} onChange={e => setDepartment(e.target.value)} className="w-full bg-black/50 border border-gray-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500" placeholder="e.g. Engineering" />
                </div>
              </div>



              <div className="flex gap-4 pt-4 border-t border-gray-800">
                <button type="button" onClick={() => setShowModal(false)} className="flex-1 bg-gray-800 hover:bg-gray-700 text-white font-medium py-3 rounded-xl transition-all">Cancel</button>
                <button type="submit" disabled={creating} className="flex-1 bg-blue-600 hover:bg-blue-500 text-white font-medium py-3 rounded-xl transition-all disabled:opacity-50">
                  {creating ? 'Saving...' : 'Add Employee'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
