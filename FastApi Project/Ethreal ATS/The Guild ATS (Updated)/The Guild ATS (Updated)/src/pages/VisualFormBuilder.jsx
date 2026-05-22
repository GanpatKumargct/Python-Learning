import React, { useState } from 'react';
import { Plus, GripVertical, Settings2, Save, Trash2, ChevronRight, LayoutTemplate } from 'lucide-react';

export function VisualFormBuilder() {
  const [formName, setFormName] = useState('New Public Application');
  const [targetEntity, setTargetEntity] = useState('candidate');
  
  const [sections, setSections] = useState([
    {
      id: 'sec-1',
      label: 'Personal Information',
      fields: [
        { id: 'f-1', name: 'name', type: 'text', label: 'Full Name', required: true, category: 'basic' },
        { id: 'f-2', name: 'email', type: 'email', label: 'Email Address', required: true, category: 'basic' }
      ]
    }
  ]);

  const [activeSection, setActiveSection] = useState('sec-1');
  const [isSaving, setIsSaving] = useState(false);

  // Field library available in the ERP
  const fieldLibrary = [
    { type: 'text', icon: 'Aa', label: 'Short Text' },
    { type: 'textarea', icon: '¶', label: 'Long Text' },
    { type: 'email', icon: '@', label: 'Email' },
    { type: 'phone', icon: '☎', label: 'Phone' },
    { type: 'file_upload', icon: '📎', label: 'File Upload' },
    { type: 'number', icon: '123', label: 'Number' },
    { type: 'dropdown', icon: '▼', label: 'Dropdown' },
  ];

  const addSection = () => {
    const newId = `sec-${Date.now()}`;
    setSections([...sections, { id: newId, label: 'New Section', fields: [] }]);
    setActiveSection(newId);
  };

  const addFieldToSection = (sectionId, fieldType) => {
    setSections(sections.map(sec => {
      if (sec.id === sectionId) {
        return {
          ...sec,
          fields: [...sec.fields, {
            id: `f-${Date.now()}`,
            name: `field_${Date.now()}`,
            type: fieldType,
            label: 'New Field',
            required: false,
            category: 'basic'
          }]
        };
      }
      return sec;
    }));
  };

  const updateField = (sectionId, fieldId, updates) => {
    setSections(sections.map(sec => {
      if (sec.id === sectionId) {
        return {
          ...sec,
          fields: sec.fields.map(f => f.id === fieldId ? { ...f, ...updates } : f)
        };
      }
      return sec;
    }));
  };

  const removeField = (sectionId, fieldId) => {
    setSections(sections.map(sec => {
      if (sec.id === sectionId) {
        return { ...sec, fields: sec.fields.filter(f => f.id !== fieldId) };
      }
      return sec;
    }));
  };

  const handleSave = () => {
    setIsSaving(true);
    // Construct the payload to send to the backend
    const payload = {
      entity_name: targetEntity,
      name: formName,
      layout: { sections: sections.map(({ label, fields }) => ({ label, fields })) }
    };
    
    console.log("Saving Form Definition JSONB:", payload);
    
    // Mock save delay
    setTimeout(() => {
      setIsSaving(false);
      alert("Form schema successfully persisted to backend JSONB!");
    }, 1000);
  };

  return (
    <div className="p-8 max-w-[1600px] mx-auto h-[calc(100vh-80px)] flex flex-col animate-fade-in">
      {/* Header */}
      <div className="flex justify-between items-end mb-6">
        <div>
          <div className="flex items-center gap-3 text-muted-foreground mb-2">
            <LayoutTemplate size={18} />
            <span>Form Engine</span>
            <ChevronRight size={14} />
            <select 
              className="bg-transparent text-primary font-medium outline-none cursor-pointer"
              value={targetEntity}
              onChange={e => setTargetEntity(e.target.value)}
            >
              <option value="candidate">Candidate Module</option>
              <option value="job_requisition">Job Requisition Module</option>
              <option value="purchase_order">Procurement Module</option>
            </select>
          </div>
          <input 
            type="text" 
            value={formName}
            onChange={(e) => setFormName(e.target.value)}
            className="text-4xl font-bold bg-transparent outline-none focus:border-b-2 focus:border-primary transition-colors min-w-[300px]"
          />
        </div>
        <button 
          onClick={handleSave}
          disabled={isSaving}
          className="bg-primary text-primary-foreground px-6 py-2.5 rounded-xl font-medium flex items-center gap-2 hover:bg-primary/90 transition-all shadow-lg shadow-primary/20 disabled:opacity-70"
        >
          {isSaving ? <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div> : <Save size={18} />}
          {isSaving ? "Publishing..." : "Publish to Engine"}
        </button>
      </div>

      {/* Workspace */}
      <div className="flex-1 flex gap-6 overflow-hidden">
        
        {/* Left: Field Library */}
        <div className="w-64 flex-shrink-0 bg-white/5 border border-white/10 rounded-2xl flex flex-col overflow-hidden backdrop-blur-md">
          <div className="p-4 border-b border-white/10 bg-black/20">
            <h3 className="font-semibold">Field Library</h3>
          </div>
          <div className="p-4 space-y-2 overflow-y-auto">
            {fieldLibrary.map((field) => (
              <div 
                key={field.type}
                onClick={() => addFieldToSection(activeSection, field.type)}
                className="flex items-center gap-3 p-3 rounded-xl border border-white/5 bg-white/5 hover:bg-white/10 hover:border-primary/30 transition-all cursor-pointer group"
              >
                <div className="w-8 h-8 rounded bg-black/40 flex items-center justify-center text-primary font-mono text-sm group-hover:scale-110 transition-transform">
                  {field.icon}
                </div>
                <span className="text-sm font-medium">{field.label}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Center: Canvas */}
        <div className="flex-1 bg-white/5 border border-white/10 rounded-2xl p-6 overflow-y-auto backdrop-blur-md">
          <div className="max-w-2xl mx-auto space-y-8">
            {sections.map((section) => (
              <div 
                key={section.id} 
                onClick={() => setActiveSection(section.id)}
                className={`p-1 rounded-2xl transition-all ${activeSection === section.id ? 'bg-primary/20 p-[2px]' : ''}`}
              >
                <div className="bg-background rounded-xl p-6 border border-white/10">
                  <input 
                    type="text" 
                    value={section.label}
                    onChange={(e) => setSections(sections.map(s => s.id === section.id ? { ...s, label: e.target.value } : s))}
                    className="text-2xl font-semibold bg-transparent outline-none mb-6 w-full focus:text-primary transition-colors"
                  />
                  
                  <div className="space-y-4">
                    {section.fields.length === 0 ? (
                      <div className="text-center py-8 border-2 border-dashed border-white/10 rounded-xl text-muted-foreground">
                        Click a field from the library to add it here.
                      </div>
                    ) : (
                      section.fields.map((field) => (
                        <div key={field.id} className="group relative flex items-start gap-4 p-4 rounded-xl border border-white/10 bg-black/20 hover:border-primary/40 transition-colors">
                          <GripVertical className="text-muted-foreground mt-2 cursor-grab active:cursor-grabbing" size={18} />
                          <div className="flex-1 space-y-3">
                            <div className="flex gap-4">
                              <div className="flex-1">
                                <label className="text-xs text-muted-foreground uppercase tracking-wider mb-1 block">Label</label>
                                <input 
                                  type="text" value={field.label} 
                                  onChange={(e) => updateField(section.id, field.id, { label: e.target.value })}
                                  className="w-full bg-transparent border-b border-white/20 focus:border-primary outline-none py-1 font-medium"
                                />
                              </div>
                              <div className="flex-1">
                                <label className="text-xs text-muted-foreground uppercase tracking-wider mb-1 block">JSON Key</label>
                                <input 
                                  type="text" value={field.name} 
                                  onChange={(e) => updateField(section.id, field.id, { name: e.target.value })}
                                  className="w-full bg-transparent border-b border-white/20 focus:border-primary outline-none py-1 font-mono text-sm text-amber-500"
                                />
                              </div>
                            </div>
                            <div className="flex items-center gap-6 pt-2">
                              <label className="flex items-center gap-2 text-sm cursor-pointer">
                                <input 
                                  type="checkbox" checked={field.required}
                                  onChange={(e) => updateField(section.id, field.id, { required: e.target.checked })}
                                  className="rounded border-white/20 text-primary focus:ring-primary bg-black/40"
                                />
                                Required Field
                              </label>
                              <div className="flex items-center gap-2 text-sm">
                                <span className="text-muted-foreground">Type:</span>
                                <span className="px-2 py-0.5 rounded bg-white/10 border border-white/10 text-xs font-mono">{field.type}</span>
                              </div>
                            </div>
                          </div>
                          <button 
                            onClick={() => removeField(section.id, field.id)}
                            className="text-muted-foreground hover:text-red-500 hover:bg-red-500/10 p-2 rounded-lg transition-colors opacity-0 group-hover:opacity-100"
                          >
                            <Trash2 size={18} />
                          </button>
                        </div>
                      ))
                    )}
                  </div>
                </div>
              </div>
            ))}
            
            <button 
              onClick={addSection}
              className="w-full py-4 border-2 border-dashed border-white/20 rounded-2xl flex flex-col items-center justify-center text-muted-foreground hover:border-primary hover:text-primary hover:bg-primary/5 transition-all"
            >
              <Plus size={24} className="mb-2" />
              <span className="font-medium">Add Layout Section</span>
            </button>
          </div>
        </div>

        {/* Right: Inspector (Placeholder for Phase 2) */}
        <div className="w-72 flex-shrink-0 bg-white/5 border border-white/10 rounded-2xl flex flex-col overflow-hidden backdrop-blur-md">
          <div className="p-4 border-b border-white/10 bg-black/20 flex items-center gap-2">
            <Settings2 size={18} />
            <h3 className="font-semibold">Properties</h3>
          </div>
          <div className="p-6 text-center text-muted-foreground space-y-4">
            <div className="w-16 h-16 bg-white/5 rounded-full mx-auto flex items-center justify-center border border-white/10">
              <Settings2 size={24} className="opacity-50" />
            </div>
            <p className="text-sm">Select a field on the canvas to configure advanced validation and dynamic visibility rules.</p>
          </div>
        </div>
      </div>
    </div>
  );
}
