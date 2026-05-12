import { useFormContext } from '../../../context/FormContext';

export const Canvas = () => {
  const { schema, activePageId, selectedFieldId, selectField } = useFormContext();

  const activePage = schema.pages.find(p => p.id === activePageId);

  return (
    <div className="flex-1 overflow-y-auto p-8 bg-gray-50/50">
      <div className="max-w-3xl mx-auto">
        <div className="glass-panel p-8 min-h-[600px]">
          <div className="border-b border-gray-200 pb-4 mb-6">
            <h1 className="text-3xl font-bold text-gray-900">{activePage?.title || 'Form'}</h1>
          </div>

          <div className="space-y-4">
            {activePage?.fields.length === 0 ? (
              <div className="h-64 border-2 border-dashed border-gray-300 rounded-xl flex flex-col items-center justify-center text-gray-400 bg-gray-50/50">
                <p className="text-lg font-medium">Empty Page</p>
                <p className="text-sm mt-1">Click fields in the sidebar to add them here.</p>
              </div>
            ) : (
              activePage?.fields.map((field) => (
                <div 
                  key={field.id}
                  onClick={() => selectField(field.id)}
                  className={`p-4 rounded-xl border-2 transition-all cursor-pointer ${selectedFieldId === field.id ? 'border-primary-500 bg-primary-50/30 shadow-md ring-4 ring-primary-500/10' : 'border-transparent hover:border-gray-200 hover:bg-gray-50'}`}
                >
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    {field.label} {field.required && <span className="text-red-500">*</span>}
                  </label>
                  
                  {field.type === 'text' || field.type === 'email' || field.type === 'number' || field.type === 'date' ? (
                    <input type={field.type} placeholder={field.placeholder} disabled className="input-field bg-white/50" />
                  ) : field.type === 'textarea' ? (
                    <textarea placeholder={field.placeholder} disabled className="input-field bg-white/50 h-24" />
                  ) : field.type === 'select' ? (
                    <select disabled className="input-field bg-white/50">
                      <option>{field.placeholder || 'Select an option'}</option>
                    </select>
                  ) : (
                    <div className="text-sm text-gray-500 italic">[{field.type} placeholder]</div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
