import { useFormContext } from '../../../context/FormContext';
import { Trash2 } from 'lucide-react';

export const PropertiesPanel = () => {
  const { schema, activePageId, selectedFieldId, updateField, removeField } = useFormContext();

  const activePage = schema.pages.find(p => p.id === activePageId);
  const selectedField = activePage?.fields.find(f => f.id === selectedFieldId);

  if (!selectedField) {
    return (
      <div className="w-80 bg-white border-l border-gray-200 p-6 flex flex-col items-center justify-center text-center text-gray-400 z-10 shadow-[-4px_0_24px_rgba(0,0,0,0.02)]">
        <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mb-4">
          <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
          </svg>
        </div>
        <p className="text-sm">Select a field to edit its properties</p>
      </div>
    );
  }

  return (
    <div className="w-80 bg-white border-l border-gray-200 overflow-y-auto flex flex-col z-10 shadow-[-4px_0_24px_rgba(0,0,0,0.02)]">
      <div className="p-4 border-b border-gray-100 flex items-center justify-between">
        <h2 className="text-sm font-bold text-gray-800 uppercase tracking-wider">Field Settings</h2>
        <button 
          onClick={() => activePageId && removeField(activePageId, selectedField.id)}
          className="text-red-500 hover:text-red-700 hover:bg-red-50 p-2 rounded-lg transition-colors"
          title="Delete Field"
        >
          <Trash2 size={18} />
        </button>
      </div>
      
      <div className="p-5 space-y-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">Field Label</label>
          <input 
            type="text" 
            value={selectedField.label}
            onChange={(e) => activePageId && updateField(activePageId, selectedField.id, { label: e.target.value })}
            className="input-field"
          />
        </div>

        {['text', 'textarea', 'number', 'email'].includes(selectedField.type) && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Placeholder</label>
            <input 
              type="text" 
              value={selectedField.placeholder || ''}
              onChange={(e) => activePageId && updateField(activePageId, selectedField.id, { placeholder: e.target.value })}
              className="input-field"
            />
          </div>
        )}

        <div className="flex items-center justify-between p-3 bg-gray-50 rounded-xl border border-gray-100">
          <label className="text-sm font-medium text-gray-700">Required Field</label>
          <label className="relative inline-flex items-center cursor-pointer">
            <input 
              type="checkbox" 
              className="sr-only peer" 
              checked={selectedField.required}
              onChange={(e) => activePageId && updateField(activePageId, selectedField.id, { required: e.target.checked })}
            />
            <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-500"></div>
          </label>
        </div>

        {['select', 'radio', 'checkbox'].includes(selectedField.type) && selectedField.options && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">Options</label>
            <div className="space-y-2">
              {selectedField.options.map((opt, idx) => (
                <div key={idx} className="flex gap-2">
                  <input 
                    type="text" 
                    value={opt}
                    onChange={(e) => {
                      const newOptions = [...(selectedField.options || [])];
                      newOptions[idx] = e.target.value;
                      activePageId && updateField(activePageId, selectedField.id, { options: newOptions });
                    }}
                    className="input-field"
                  />
                  <button 
                    onClick={() => {
                      const newOptions = selectedField.options?.filter((_, i) => i !== idx);
                      activePageId && updateField(activePageId, selectedField.id, { options: newOptions });
                    }}
                    className="p-2 text-gray-400 hover:text-red-500 rounded border border-gray-200"
                  >
                    ×
                  </button>
                </div>
              ))}
              <button 
                onClick={() => {
                  const newOptions = [...(selectedField.options || []), `Option ${(selectedField.options?.length || 0) + 1}`];
                  activePageId && updateField(activePageId, selectedField.id, { options: newOptions });
                }}
                className="w-full py-2 text-sm text-primary-600 bg-primary-50 rounded border border-primary-100 hover:bg-primary-100 font-medium transition-colors"
              >
                + Add Option
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
