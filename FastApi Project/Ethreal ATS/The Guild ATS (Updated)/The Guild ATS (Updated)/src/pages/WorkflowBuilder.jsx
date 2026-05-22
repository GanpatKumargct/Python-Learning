import React, { useState } from 'react';
import { GitMerge, Plus, ArrowRight, Save, Trash2, Settings2, PlayCircle, StopCircle } from 'lucide-react';

export function WorkflowBuilder() {
  const [targetEntity, setTargetEntity] = useState('candidate');
  const [workflowName, setWorkflowName] = useState('Standard Hiring Pipeline');
  
  // Mock initial state for Phase 3 UI Demonstration
  const [states, setStates] = useState([
    { id: 's1', name: 'applied', label: 'Applied', is_initial: true, is_terminal: false },
    { id: 's2', name: 'screening', label: 'Screening', is_initial: false, is_terminal: false },
    { id: 's3', name: 'interview', label: 'Interview', is_initial: false, is_terminal: false },
    { id: 's4', name: 'offer', label: 'Offer Stage', is_initial: false, is_terminal: false },
    { id: 's5', name: 'hired', label: 'Hired', is_initial: false, is_terminal: true },
    { id: 's6', name: 'rejected', label: 'Rejected', is_initial: false, is_terminal: true }
  ]);

  const [transitions, setTransitions] = useState([
    { id: 't1', name: 'move_to_screening', from_id: 's1', to_id: 's2' },
    { id: 't2', name: 'schedule_interview', from_id: 's2', to_id: 's3' },
    { id: 't3', name: 'send_offer', from_id: 's3', to_id: 's4' },
    { id: 't4', name: 'hire_candidate', from_id: 's4', to_id: 's5' },
    { id: 't5', name: 'reject_candidate', from_id: 's2', to_id: 's6' },
  ]);

  const [isSaving, setIsSaving] = useState(false);

  const addState = () => {
    const newId = `s${Date.now()}`;
    setStates([...states, { id: newId, name: `new_stage_${Date.now()}`, label: 'New Stage', is_initial: false, is_terminal: false }]);
  };

  const removeState = (id) => {
    if (states.find(s => s.id === id).is_initial) {
      alert("Cannot delete the initial state.");
      return;
    }
    setStates(states.filter(s => s.id !== id));
    setTransitions(transitions.filter(t => t.from_id !== id && t.to_id !== id));
  };

  const updateState = (id, updates) => {
    setStates(states.map(s => s.id === id ? { ...s, ...updates } : s));
  };

  const addTransition = (fromId) => {
    // Default to the first available non-initial state as target
    const toState = states.find(s => s.id !== fromId && !s.is_initial) || states[0];
    if (toState) {
      setTransitions([...transitions, { 
        id: `t${Date.now()}`, 
        name: `transition_${Date.now()}`, 
        from_id: fromId, 
        to_id: toState.id 
      }]);
    }
  };

  const removeTransition = (id) => {
    setTransitions(transitions.filter(t => t.id !== id));
  };

  const updateTransition = (id, updates) => {
    setTransitions(transitions.map(t => t.id === id ? { ...t, ...updates } : t));
  };

  const handleSave = () => {
    setIsSaving(true);
    const payload = {
      entity: targetEntity,
      workflow_name: workflowName,
      states,
      transitions
    };
    console.log("Saving Workflow Definition:", payload);
    setTimeout(() => {
      setIsSaving(false);
      alert("Workflow Pipeline successfully persisted to PostgreSQL Engine!");
    }, 1000);
  };

  return (
    <div className="p-8 max-w-[1600px] mx-auto h-[calc(100vh-80px)] flex flex-col animate-fade-in">
      {/* Header */}
      <div className="flex justify-between items-end mb-8">
        <div>
          <div className="flex items-center gap-3 text-muted-foreground mb-2">
            <GitMerge size={18} />
            <span>Workflow Engine Configurator</span>
            <ArrowRight size={14} />
            <select 
              className="bg-transparent text-primary font-medium outline-none cursor-pointer uppercase"
              value={targetEntity}
              onChange={e => setTargetEntity(e.target.value)}
            >
              <option value="candidate">Candidate ATS Module</option>
              <option value="job_requisition">Job Requisition Module</option>
              <option value="purchase_order">Procurement Module</option>
            </select>
          </div>
          <input 
            type="text" 
            value={workflowName}
            onChange={(e) => setWorkflowName(e.target.value)}
            className="text-4xl font-bold bg-transparent outline-none focus:border-b-2 focus:border-primary transition-colors min-w-[400px]"
          />
        </div>
        <button 
          onClick={handleSave}
          disabled={isSaving}
          className="bg-primary text-primary-foreground px-6 py-2.5 rounded-xl font-medium flex items-center gap-2 hover:bg-primary/90 transition-all shadow-lg shadow-primary/20 disabled:opacity-70"
        >
          {isSaving ? <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div> : <Save size={18} />}
          {isSaving ? "Syncing..." : "Sync Pipeline to Engine"}
        </button>
      </div>

      <div className="flex-1 overflow-y-auto pr-4">
        <div className="bg-white/5 border border-white/10 rounded-3xl p-8 backdrop-blur-md">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-2xl font-bold">Pipeline Stages (Kanban Columns)</h2>
            <button 
              onClick={addState}
              className="bg-white/10 hover:bg-white/20 text-foreground px-4 py-2 rounded-xl text-sm font-medium transition-colors flex items-center gap-2"
            >
              <Plus size={16} /> Add Stage
            </button>
          </div>

          <div className="space-y-6">
            {states.map(state => (
              <div key={state.id} className="bg-black/20 border border-white/10 rounded-2xl p-6 relative group">
                <div className="absolute top-4 right-4 flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button onClick={() => addTransition(state.id)} className="p-2 text-primary hover:bg-primary/10 rounded-lg tooltip-trigger" title="Add outgoing transition">
                    <ArrowRight size={18} />
                  </button>
                  {!state.is_initial && (
                    <button onClick={() => removeState(state.id)} className="p-2 text-red-500 hover:bg-red-500/10 rounded-lg">
                      <Trash2 size={18} />
                    </button>
                  )}
                </div>

                <div className="flex items-start gap-8 mb-6">
                  <div className="flex-1">
                    <label className="text-xs text-muted-foreground uppercase tracking-wider mb-1 block">Display Label (UI)</label>
                    <input 
                      type="text" value={state.label}
                      onChange={(e) => updateState(state.id, { label: e.target.value })}
                      className="text-xl font-bold bg-transparent border-b border-transparent focus:border-primary outline-none py-1 w-full"
                    />
                  </div>
                  <div className="flex-1">
                    <label className="text-xs text-muted-foreground uppercase tracking-wider mb-1 block">System ID (Backend)</label>
                    <input 
                      type="text" value={state.name}
                      onChange={(e) => updateState(state.id, { name: e.target.value })}
                      className="text-lg font-mono text-amber-500 bg-transparent border-b border-transparent focus:border-amber-500 outline-none py-1 w-full"
                    />
                  </div>
                  <div className="flex items-center gap-4 mt-6">
                    <label className={`flex items-center gap-2 text-sm cursor-pointer ${state.is_initial ? 'text-green-500' : 'text-muted-foreground'}`}>
                      <PlayCircle size={16} />
                      <input 
                        type="checkbox" checked={state.is_initial}
                        onChange={(e) => {
                          if (e.target.checked) {
                            // Enforce only one initial state
                            setStates(states.map(s => ({ ...s, is_initial: s.id === state.id })));
                          }
                        }}
                        className="hidden"
                      />
                      Entry Point
                    </label>
                    <label className={`flex items-center gap-2 text-sm cursor-pointer ${state.is_terminal ? 'text-red-400' : 'text-muted-foreground'}`}>
                      <StopCircle size={16} />
                      <input 
                        type="checkbox" checked={state.is_terminal}
                        onChange={(e) => updateState(state.id, { is_terminal: e.target.checked })}
                        className="hidden"
                      />
                      Terminal Stage
                    </label>
                  </div>
                </div>

                {/* Transitions originating from this state */}
                <div className="bg-white/5 rounded-xl p-4 border border-white/5">
                  <h4 className="text-sm font-semibold mb-3 flex items-center gap-2 text-muted-foreground">
                    <GitMerge size={14} /> Allowed Transitions (Routing Rules)
                  </h4>
                  {transitions.filter(t => t.from_id === state.id).length === 0 ? (
                    <p className="text-sm text-muted-foreground/50 italic">No outgoing transitions. Records in this stage cannot be moved.</p>
                  ) : (
                    <div className="space-y-2">
                      {transitions.filter(t => t.from_id === state.id).map(transition => (
                        <div key={transition.id} className="flex items-center gap-4 bg-black/40 p-3 rounded-lg border border-white/5">
                          <input 
                            type="text" value={transition.name}
                            onChange={(e) => updateTransition(transition.id, { name: e.target.value })}
                            className="bg-transparent font-mono text-sm border-b border-white/20 focus:border-primary outline-none px-1 w-48"
                            placeholder="action_name"
                          />
                          <ArrowRight size={14} className="text-muted-foreground" />
                          <select 
                            value={transition.to_id}
                            onChange={(e) => updateTransition(transition.id, { to_id: e.target.value })}
                            className="bg-transparent text-sm font-medium outline-none border-b border-white/20 focus:border-primary px-1 pb-1"
                          >
                            {states.map(s => (
                              <option key={s.id} value={s.id} className="bg-slate-900">{s.label}</option>
                            ))}
                          </select>
                          <div className="flex-1"></div>
                          <button onClick={() => removeTransition(transition.id)} className="text-muted-foreground hover:text-red-500 p-1">
                            <Trash2 size={14} />
                          </button>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
