import React, { useState } from 'react';
import { DndContext, closestCenter, KeyboardSensor, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
import { arrayMove, SortableContext, sortableKeyboardCoordinates, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { SortableField } from '../components/FormBuilder/SortableField';
import apiClient from '../../../lib/apiClient';

const FIELD_TYPES = [
  { type: 'text', label: 'Short Text', icon: 'M4 6h16M4 12h16M4 18h7' },
  { type: 'textarea', label: 'Long Text', icon: 'M4 6h16M4 12h16m-7 6h7' },
  { type: 'number', label: 'Number', icon: 'M7 20l4-16m2 16l4-16M6 9h14M4 15h14' },
  { type: 'date', label: 'Date', icon: 'M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z' },
  { type: 'file', label: 'File Upload', icon: 'M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12' },
];

export default function FormBuilderPage() {
  const [formTitle, setFormTitle] = useState('New Candidate Application');
  const [formDescription, setFormDescription] = useState('Please fill out your details carefully.');
  const [fields, setFields] = useState([]);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState(null);

  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates })
  );

  const addField = (fieldType) => {
    const newId = `field_${Date.now()}`;
    const newField = {
      id: newId,
      field_key: `field_${fields.length + 1}`,
      label: `New ${fieldType} Field`,
      field_type: fieldType,
      is_required: false,
      column_type: fieldType === 'number' ? 'INTEGER' : fieldType === 'date' ? 'DATE' : 'TEXT'
    };
    setFields([...fields, newField]);
  };

  const removeField = (id) => {
    setFields(fields.filter(f => f.id !== id));
  };

  const updateField = (id, updatedField) => {
    setFields(fields.map(f => f.id === id ? updatedField : f));
  };

  const handleDragEnd = (event) => {
    const { active, over } = event;
    if (active.id !== over.id) {
      setFields((items) => {
        const oldIndex = items.findIndex((i) => i.id === active.id);
        const newIndex = items.findIndex((i) => i.id === over.id);
        return arrayMove(items, oldIndex, newIndex);
      });
    }
  };

  const [isPreview, setIsPreview] = useState(false);

  const handleSaveForm = async () => {
    if (fields.length === 0) {
      setMessage({ type: 'error', text: 'Please add at least one field.' });
      return;
    }
    setSaving(true);
    setMessage(null);

    try {
      const payload = {
        title: formTitle,
        description: formDescription,
        module: 'ats',
        fields: fields.map((f, index) => ({
          field_key: f.field_key,
          label: f.label,
          field_type: f.field_type,
          is_required: f.is_required,
          display_order: index,
          column_type: f.column_type
        }))
      };

      const res = await apiClient.post('/forms/', payload);
      setMessage({ type: 'success', text: `Success! Table ${res.data.response_table} created dynamically.` });
    } catch (err) {
      setMessage({ type: 'error', text: err.response?.data?.detail || 'Failed to save form.' });
    } finally {
      setSaving(false);
    }
  };

  const renderPreviewField = (field) => {
    const inputClasses = "w-full bg-gray-950 border border-gray-800 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-blue-500 transition-colors mt-2";
    
    return (
      <div key={field.id} className="mb-6">
        <label className="block text-sm font-medium text-gray-300">
          {field.label} {field.is_required && <span className="text-red-500">*</span>}
        </label>
        {field.field_type === 'text' && <input type="text" className={inputClasses} placeholder={`Enter ${field.label}`} />}
        {field.field_type === 'textarea' && <textarea className={inputClasses} rows={4} placeholder={`Enter ${field.label}`} />}
        {field.field_type === 'number' && <input type="number" className={inputClasses} placeholder="0" />}
        {field.field_type === 'date' && <input type="date" className={inputClasses} />}
        {field.field_type === 'file' && (
          <div className={`${inputClasses} flex items-center justify-center border-dashed text-gray-500 bg-gray-950/50 cursor-pointer hover:border-blue-500/50`}>
            <span className="text-sm">Click to upload file</span>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-[#0A0A0A] text-white flex flex-col md:flex-row">
      {/* Sidebar Tools */}
      <aside className="w-full md:w-72 bg-gray-950 border-r border-gray-800 p-6 flex flex-col sticky top-0 h-screen overflow-y-auto">
        <div className="mb-8">
          <h2 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-purple-500">
            Form Builder
          </h2>
          <p className="text-xs text-gray-500 mt-1">Drag and drop to build schemas.</p>
        </div>

        <div className="space-y-4 flex-1">
          <h3 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Components</h3>
          <div className="grid grid-cols-1 gap-2">
            {FIELD_TYPES.map((type) => (
              <button
                key={type.type}
                onClick={() => { addField(type.type); setIsPreview(false); }}
                className="flex items-center gap-3 bg-gray-900 border border-gray-800 hover:border-blue-500/50 hover:bg-gray-800 p-3 rounded-xl transition-all text-sm font-medium text-gray-300 text-left w-full group"
              >
                <div className="text-gray-500 group-hover:text-blue-400 transition-colors">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d={type.icon} />
                  </svg>
                </div>
                {type.label}
              </button>
            ))}
          </div>
        </div>

        <button 
          onClick={handleSaveForm}
          disabled={saving}
          className="w-full mt-6 bg-blue-600 hover:bg-blue-500 text-white font-semibold py-3 px-4 rounded-xl shadow-lg shadow-blue-500/20 transition-all disabled:opacity-50 flex justify-center items-center gap-2"
        >
          {saving ? 'Creating Table...' : 'Publish Form Schema'}
        </button>
      </aside>

      {/* Main Canvas */}
      <main className="flex-1 p-8 lg:p-12 overflow-y-auto max-w-4xl mx-auto w-full relative">
        <div className="absolute top-8 right-12 flex bg-gray-900 rounded-xl p-1 border border-gray-800">
          <button 
            onClick={() => setIsPreview(false)}
            className={`px-4 py-1.5 text-sm font-medium rounded-lg transition-all ${!isPreview ? 'bg-gray-800 text-white shadow' : 'text-gray-400 hover:text-white'}`}
          >
            Edit
          </button>
          <button 
            onClick={() => setIsPreview(true)}
            className={`px-4 py-1.5 text-sm font-medium rounded-lg transition-all flex items-center gap-2 ${isPreview ? 'bg-gray-800 text-white shadow' : 'text-gray-400 hover:text-white'}`}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            Preview
          </button>
        </div>

        {message && (
          <div className={`mb-6 p-4 rounded-xl border ${message.type === 'success' ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400' : 'bg-red-500/10 border-red-500/20 text-red-400'}`}>
            {message.text}
          </div>
        )}

        <div className="mb-10 space-y-4 max-w-2xl mt-4">
          <input
            type="text"
            value={formTitle}
            onChange={(e) => setFormTitle(e.target.value)}
            disabled={isPreview}
            className={`w-full bg-transparent text-4xl font-extrabold text-white placeholder-gray-600 focus:outline-none focus:border-b-2 focus:border-blue-500 pb-2 transition-all ${isPreview ? 'border-b-0 disabled:text-white' : ''}`}
            placeholder="Form Title"
          />
          <textarea
            value={formDescription}
            onChange={(e) => setFormDescription(e.target.value)}
            disabled={isPreview}
            className={`w-full bg-transparent text-gray-400 placeholder-gray-600 focus:outline-none focus:border-b-2 focus:border-blue-500 pb-2 transition-all resize-none ${isPreview ? 'border-b-0 disabled:text-gray-400' : ''}`}
            placeholder="Form Description"
            rows={2}
          />
        </div>

        {fields.length === 0 ? (
          <div className="border-2 border-dashed border-gray-800 rounded-3xl p-16 flex flex-col items-center justify-center text-center">
            <div className="w-16 h-16 bg-gray-900 rounded-full flex items-center justify-center mb-4">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
            </div>
            <h3 className="text-xl font-bold text-gray-300 mb-2">Your form is empty</h3>
            <p className="text-gray-500 max-w-sm">Click the components on the left sidebar to add them to your new ATS application form.</p>
          </div>
        ) : isPreview ? (
          <div className="max-w-2xl bg-gray-900/40 p-8 rounded-3xl border border-gray-800 shadow-2xl backdrop-blur-sm animate-fade-in">
            <form onSubmit={e => e.preventDefault()}>
              {fields.map(renderPreviewField)}
              <div className="mt-8 pt-6 border-t border-gray-800">
                <button type="button" className="bg-gradient-to-r from-blue-600 to-purple-600 text-white font-medium px-6 py-3 rounded-xl shadow-lg opacity-80 cursor-not-allowed w-full">
                  Submit Application (Preview)
                </button>
              </div>
            </form>
          </div>
        ) : (
          <div className="space-y-4 max-w-2xl">
            <DndContext sensors={sensors} collisionDetection={closestCenter} onDragEnd={handleDragEnd}>
              <SortableContext items={fields.map(f => f.id)} strategy={verticalListSortingStrategy}>
                {fields.map((field) => (
                  <SortableField 
                    key={field.id} 
                    id={field.id} 
                    field={field} 
                    onRemove={removeField}
                    onUpdate={updateField}
                  />
                ))}
              </SortableContext>
            </DndContext>
          </div>
        )}
      </main>
    </div>
  );
}
