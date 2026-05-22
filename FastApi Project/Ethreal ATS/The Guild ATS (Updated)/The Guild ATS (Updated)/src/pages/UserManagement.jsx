import React, { useState, useEffect } from 'react';
import { UserPlus, Shield, Check, X, ShieldAlert } from 'lucide-react';

export function UserManagement() {
  const [users, setUsers] = useState([]);
  const [entities, setEntities] = useState([]);
  const [roles, setRoles] = useState([]);
  
  const [isAddingUser, setIsAddingUser] = useState(false);
  const [newUser, setNewUser] = useState({ name: '', email: '', role_id: '' });
  
  const [selectedRole, setSelectedRole] = useState(null);
  
  // Mock data for Phase 1 UI Demonstration
  useEffect(() => {
    // These would normally be fetched from the FastApi Backend
    setEntities(['candidate', 'job_requisition', 'purchase_order', 'system']);
    setRoles([
      { id: '1', name: 'super_admin', label: 'System Administrator' },
      { id: '2', name: 'ptc', label: 'People & Talent Coordinator' },
      { id: '3', name: 'hiring_manager', label: 'Hiring Manager' }
    ]);
    setUsers([
      { id: 'u1', name: 'Admin User', email: 'admin@ethereal.com', role_id: '1' },
      { id: 'u2', name: 'Jane HR', email: 'jane@ethereal.com', role_id: '2' }
    ]);
  }, []);

  const handleAddUser = (e) => {
    e.preventDefault();
    setUsers([...users, { ...newUser, id: Date.now().toString() }]);
    setIsAddingUser(false);
    setNewUser({ name: '', email: '', role_id: '' });
  };

  const actions = ['create', 'read', 'update', 'delete', 'transition'];

  return (
    <div className="p-8 max-w-7xl mx-auto space-y-8 animate-fade-in">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">Access Engine & Users</h1>
          <p className="text-muted-foreground mt-1">Manage personnel and granular RBAC policies.</p>
        </div>
        <button 
          onClick={() => setIsAddingUser(true)}
          className="bg-primary text-primary-foreground px-4 py-2 rounded-xl flex items-center gap-2 hover:bg-primary/90 transition-all shadow-lg shadow-primary/20"
        >
          <UserPlus size={18} /> Add User
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Users List */}
        <div className="lg:col-span-1 bg-white/5 border border-white/10 rounded-2xl p-6 backdrop-blur-md">
          <h2 className="text-xl font-semibold mb-6 flex items-center gap-2"><Shield size={20} className="text-primary"/> Active Personnel</h2>
          <div className="space-y-4">
            {users.map(user => {
              const role = roles.find(r => r.id === user.role_id);
              return (
                <div key={user.id} className="p-4 rounded-xl bg-black/20 border border-white/5 hover:border-primary/30 transition-colors cursor-pointer" onClick={() => setSelectedRole(role)}>
                  <div className="font-medium text-lg">{user.name}</div>
                  <div className="text-sm text-muted-foreground mb-2">{user.email}</div>
                  <div className="inline-block px-2.5 py-0.5 rounded-full bg-primary/10 text-primary text-xs font-semibold border border-primary/20">
                    {role?.label || 'No Role'}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Dynamic Permissions Matrix */}
        <div className="lg:col-span-2 bg-white/5 border border-white/10 rounded-2xl p-6 backdrop-blur-md">
          <h2 className="text-xl font-semibold mb-2 flex items-center gap-2">
            <ShieldAlert size={20} className="text-amber-500"/> Permission Matrix
          </h2>
          <p className="text-sm text-muted-foreground mb-6">
            {selectedRole 
              ? `Defining granular access for role: ${selectedRole.label}` 
              : "Select a user to view or edit their role's permissions."}
          </p>

          {selectedRole ? (
            <div className="overflow-x-auto">
              <table className="w-full text-sm text-left">
                <thead className="text-xs text-muted-foreground uppercase bg-black/40">
                  <tr>
                    <th className="px-6 py-4 rounded-tl-xl">Entity Module</th>
                    {actions.map(action => (
                      <th key={action} className="px-6 py-4 text-center">{action}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {entities.map(entity => (
                    <tr key={entity} className="border-b border-white/5 hover:bg-white/5">
                      <td className="px-6 py-4 font-medium capitalize">{entity.replace('_', ' ')}</td>
                      {actions.map(action => {
                        // Nobody manually creates candidates (done via public form)
                        const isInvalidAction = entity === 'candidate' && action === 'create';
                        
                        // Mock permission check
                        const hasAccess = selectedRole.name === 'super_admin' || (selectedRole.name === 'ptc' && entity === 'candidate');
                        
                        if (isInvalidAction) {
                          return (
                            <td key={`${entity}-${action}`} className="px-6 py-4 text-center">
                              <span className="text-muted-foreground/50 text-xs italic">N/A</span>
                            </td>
                          );
                        }

                        return (
                          <td key={`${entity}-${action}`} className="px-6 py-4 text-center">
                            <button 
                              className={`w-6 h-6 rounded flex items-center justify-center mx-auto transition-colors ${hasAccess ? 'bg-green-500/20 text-green-500 border border-green-500/30' : 'bg-red-500/10 text-red-500/40 border border-red-500/20 hover:border-red-500/50 hover:text-red-500'}`}
                            >
                              {hasAccess ? <Check size={14} /> : <X size={14} />}
                            </button>
                          </td>
                        );
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
              <div className="mt-6 flex justify-end">
                <button className="bg-primary text-primary-foreground px-6 py-2 rounded-xl text-sm font-medium hover:bg-primary/90 transition-colors">
                  Save Matrix to Engine
                </button>
              </div>
            </div>
          ) : (
            <div className="h-64 flex items-center justify-center border-2 border-dashed border-white/10 rounded-xl">
              <span className="text-muted-foreground">Select a role to configure permissions</span>
            </div>
          )}
        </div>
      </div>

      {/* Add User Modal */}
      {isAddingUser && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-background border border-white/10 rounded-2xl p-6 w-full max-w-md shadow-2xl animate-zoom-in">
            <h3 className="text-xl font-bold mb-4">Provision New User</h3>
            <form onSubmit={handleAddUser} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Full Name</label>
                <input 
                  required type="text" value={newUser.name} onChange={e => setNewUser({...newUser, name: e.target.value})}
                  className="w-full px-3 py-2 bg-black/20 border border-white/10 rounded-lg focus:ring-1 focus:ring-primary outline-none" 
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Email</label>
                <input 
                  required type="email" value={newUser.email} onChange={e => setNewUser({...newUser, email: e.target.value})}
                  className="w-full px-3 py-2 bg-black/20 border border-white/10 rounded-lg focus:ring-1 focus:ring-primary outline-none" 
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Assign Role</label>
                <input 
                  required 
                  type="text" 
                  placeholder="e.g., HR_MANAGER"
                  value={newUser.role_id} 
                  onChange={e => setNewUser({...newUser, role_id: e.target.value.toUpperCase()})}
                  className="w-full px-3 py-2 bg-black/20 border border-white/10 rounded-lg focus:ring-1 focus:ring-primary outline-none uppercase" 
                />
                <p className="text-xs text-muted-foreground mt-1.5">
                  Type any custom role name. Use UPPERCASE and underscores (e.g., FINANCE_LEAD, RECRUITER).
                </p>
              </div>
              <div className="flex justify-end gap-3 pt-4">
                <button type="button" onClick={() => setIsAddingUser(false)} className="px-4 py-2 rounded-lg hover:bg-white/5 transition-colors">Cancel</button>
                <button type="submit" className="bg-primary text-primary-foreground px-4 py-2 rounded-lg hover:bg-primary/90 transition-colors">Provision</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
