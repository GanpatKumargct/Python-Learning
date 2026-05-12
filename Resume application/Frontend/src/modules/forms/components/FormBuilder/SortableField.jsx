import React from 'react';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';

export function SortableField({ id, field, onRemove, onUpdate }) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
  } = useSortable({ id });

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  };

  return (
    <div 
      ref={setNodeRef} 
      style={style} 
      className="bg-gray-900 border border-gray-800 rounded-xl p-5 mb-4 group hover:border-gray-700 transition-colors shadow-sm"
    >
      <div className="flex justify-between items-center mb-4">
        <div className="flex items-center gap-3">
          <div {...attributes} {...listeners} className="cursor-grab active:cursor-grabbing p-1.5 text-gray-500 hover:text-gray-300 rounded-md hover:bg-gray-800">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8h16M4 16h16" />
            </svg>
          </div>
          <span className="text-xs font-bold uppercase tracking-wider text-blue-400 bg-blue-500/10 px-2.5 py-1 rounded-md">
            {field.field_type}
          </span>
        </div>
        <button onClick={() => onRemove(id)} className="text-red-400/70 hover:text-red-400 p-1.5 rounded-md hover:bg-red-500/10 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
        </button>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="space-y-1.5">
          <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wider">Field Label</label>
          <input 
            type="text" 
            value={field.label}
            onChange={(e) => onUpdate(id, { ...field, label: e.target.value })}
            className="w-full bg-black/40 border border-gray-800 rounded-lg px-3 py-2.5 text-white text-sm focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-colors"
            placeholder="e.g. Years of Experience"
          />
        </div>
        <div className="space-y-1.5">
          <label className="text-[10px] font-bold text-gray-500 uppercase tracking-wider">Database Key</label>
          <input 
            type="text" 
            value={field.field_key}
            onChange={(e) => onUpdate(id, { ...field, field_key: e.target.value.replace(/[^a-zA-Z0-9_]/g, '').toLowerCase() })}
            className="w-full bg-black/40 border border-gray-800 rounded-lg px-3 py-2.5 text-gray-300 text-sm focus:outline-none focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/50 transition-colors font-mono"
            placeholder="e.g. years_exp"
          />
        </div>
      </div>
      
      <div className="mt-5 flex items-center gap-2">
        <input 
          type="checkbox" 
          id={`req-${id}`}
          checked={field.is_required}
          onChange={(e) => onUpdate(id, { ...field, is_required: e.target.checked })}
          className="w-4 h-4 rounded border-gray-700 bg-gray-900 text-blue-500 focus:ring-blue-500 focus:ring-offset-gray-900 cursor-pointer"
        />
        <label htmlFor={`req-${id}`} className="text-sm text-gray-300 select-none cursor-pointer hover:text-white transition-colors">Required field</label>
      </div>
    </div>
  );
}
