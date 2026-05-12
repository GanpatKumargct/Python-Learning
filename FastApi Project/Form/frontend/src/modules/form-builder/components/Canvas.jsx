import { useFormContext } from '../../../context/FormContext';

export const Canvas = () => {
  const { schema, activePageId, selectedFieldId, selectField, updateField } = useFormContext();

  const activePage = schema.pages.find(p => p.id === activePageId);

  return (
    <div className="flex-1 overflow-y-auto p-4 sm:p-8 bg-googleBg">
      <div className="max-w-3xl mx-auto space-y-4 pb-20">
        
        {/* Form Title Card */}
        <div className="bg-white border border-gray-300 rounded-lg shadow-sm border-t-8 border-t-primary-600 p-6 relative">
          <input 
            type="text" 
            value={activePage?.title || 'Untitled form'}
            onChange={(e) => {}} /* You would typically bind this to update form title */
            className="text-3xl font-medium w-full border-b border-transparent hover:border-gray-200 focus:border-primary-600 focus:outline-none py-2 transition-colors mb-2"
          />
          <input 
            type="text"
            placeholder="Form description"
            className="text-sm text-gray-600 w-full border-b border-transparent hover:border-gray-200 focus:border-primary-600 focus:outline-none py-1 transition-colors"
          />
        </div>

        {/* Form Fields list */}
        {activePage?.fields.length === 0 ? (
          <div className="bg-white border border-gray-300 rounded-lg shadow-sm p-10 text-center text-gray-500">
            <p>Add a field from the sidebar to get started.</p>
          </div>
        ) : (
          activePage?.fields.map((field) => (
            <div 
              key={field.id}
              onClick={() => selectField(field.id)}
              className={`p-6 cursor-pointer ${selectedFieldId === field.id ? 'google-card-active' : 'google-card'}`}
            >
              <div className="flex flex-col gap-4">
                <input 
                  type="text" 
                  value={field.label}
                  onChange={(e) => updateField(activePageId, field.id, { label: e.target.value })}
                  placeholder="Question"
                  className="text-base font-medium bg-gray-50 p-3 rounded focus:bg-gray-100 focus:outline-none focus:border-b-2 focus:border-primary-600 w-full sm:w-2/3"
                />
                
                {field.type === 'text' || field.type === 'email' || field.type === 'number' || field.type === 'date' ? (
                  <input type={field.type} placeholder="Short answer text" disabled className="input-google w-1/2 mt-2" />
                ) : field.type === 'textarea' ? (
                  <textarea placeholder="Long answer text" disabled className="input-google w-3/4 h-10 mt-2 resize-none" />
                ) : field.type === 'select' ? (
                  <div className="border border-gray-300 p-2 rounded w-1/2 flex justify-between items-center text-gray-500 mt-2 bg-gray-50">
                    <span>{field.options?.[0] || 'Option 1'}</span>
                    <span>▼</span>
                  </div>
                ) : field.type === 'radio' || field.type === 'checkbox' ? (
                  <div className="space-y-3 mt-2">
                    {field.options?.map((opt, idx) => (
                      <div key={idx} className="flex items-center gap-3">
                        <div className={`w-4 h-4 border border-gray-400 ${field.type === 'radio' ? 'rounded-full' : 'rounded-sm'}`}></div>
                        <span className="text-gray-700">{opt}</span>
                      </div>
                    ))}
                  </div>
                ) : null}
              </div>

              {/* Action Footer (Only visible when active) */}
              {selectedFieldId === field.id && (
                <div className="mt-6 pt-4 border-t border-gray-200 flex justify-end items-center gap-4 text-gray-500">
                  <div className="flex items-center gap-2 border-l pl-4 border-gray-200">
                    <span className="text-sm">Required</span>
                    <label className="relative inline-flex items-center cursor-pointer">
                      <input 
                        type="checkbox" 
                        className="sr-only peer" 
                        checked={field.required}
                        onChange={(e) => updateField(activePageId, field.id, { required: e.target.checked })}
                      />
                      <div className="w-9 h-5 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-primary-600"></div>
                    </label>
                  </div>
                </div>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
};
