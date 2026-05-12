import { useFormContext } from '../../../context/FormContext';
import { Trash2, GripVertical, Settings2 } from 'lucide-react';

export const PropertiesPanel = () => {
  const { schema, activePageId, selectedFieldId, updateField, removeField } = useFormContext();

  const activePage = schema.pages.find(p => p.id === activePageId);
  const selectedField = activePage?.fields.find(f => f.id === selectedFieldId);

  if (!selectedField) {
    return (
      <div className="w-80 bg-white border-l border-gray-200 p-6 flex flex-col items-center justify-center text-center text-gray-500 z-10 shadow-[-4px_0_24px_rgba(0,0,0,0.02)] hidden lg:flex">
        <Settings2 size={48} className="text-gray-200 mb-4" />
        <p className="text-sm font-medium">Field Settings</p>
        <p className="text-xs text-gray-400 mt-2">Select a field on the canvas to configure it</p>
      </div>
    );
  }

  return (
    <div className="w-80 bg-white border-l border-gray-200 overflow-y-auto flex flex-col z-10 shadow-[-4px_0_24px_rgba(0,0,0,0.02)]">
      <div className="p-5 border-b border-gray-200 flex items-center justify-between bg-gray-50">
        <h2 className="text-sm font-bold text-gray-700 tracking-wide">Options</h2>
        <button 
          onClick={() => activePageId && removeField(activePageId, selectedField.id)}
          className="text-gray-400 hover:text-red-600 hover:bg-red-50 p-2 rounded-full transition-colors"
          title="Delete Field"
        >
          <Trash2 size={18} />
        </button>
      </div>
      
      <div className="p-6 space-y-6">
        <div>
          <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Field Type</label>
          <div className="p-3 bg-gray-50 rounded border border-gray-200 text-sm font-medium text-gray-700 capitalize">
            {selectedField.type}
          </div>
        </div>

        {['text', 'textarea', 'number', 'email'].includes(selectedField.type) && (
          <div>
            <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">Placeholder Text</label>
            <input 
              type="text" 
              placeholder="E.g., enter your email"
              value={selectedField.placeholder || ''}
              onChange={(e) => activePageId && updateField(activePageId, selectedField.id, { placeholder: e.target.value })}
              className="w-full px-3 py-2 border border-gray-300 rounded focus:outline-none focus:border-primary-600 focus:ring-1 focus:ring-primary-600 text-sm transition-colors"
            />
          </div>
        )}

        {['select', 'radio', 'checkbox'].includes(selectedField.type) && selectedField.options && (
          <div>
            <label className="block text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">Choices</label>
            <div className="space-y-3">
              {selectedField.options.map((opt, idx) => (
                <div key={idx} className="flex gap-2 items-center group">
                  <GripVertical size={16} className="text-gray-300 cursor-grab" />
                  <input 
                    type="text" 
                    value={opt}
                    onChange={(e) => {
                      const newOptions = [...(selectedField.options || [])];
                      newOptions[idx] = e.target.value;
                      activePageId && updateField(activePageId, selectedField.id, { options: newOptions });
                    }}
                    className="w-full px-0 py-1 border-b border-transparent hover:border-gray-300 focus:border-primary-600 focus:outline-none text-sm transition-colors"
                  />
                  <button 
                    onClick={() => {
                      const newOptions = selectedField.options?.filter((_, i) => i !== idx);
                      activePageId && updateField(activePageId, selectedField.id, { options: newOptions });
                    }}
                    className="p-1 text-gray-300 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity"
                  >
                    ×
                  </button>
                </div>
              ))}
              <div className="pt-2 pl-6">
                <button 
                  onClick={() => {
                    const newOptions = [...(selectedField.options || []), `Option ${(selectedField.options?.length || 0) + 1}`];
                    activePageId && updateField(activePageId, selectedField.id, { options: newOptions });
                  }}
                  className="text-sm text-primary-600 font-medium hover:underline focus:outline-none"
                >
                  Add option
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
