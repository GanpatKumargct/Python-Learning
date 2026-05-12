import { Type, AlignLeft, Hash, Mail, CheckSquare, CircleDot, Calendar, ChevronDown } from 'lucide-react';
import { useFormContext } from '../../../context/FormContext';

const fieldTypes = [
  { type: 'text', label: 'Short Text', icon: <Type size={18} /> },
  { type: 'textarea', label: 'Long Text', icon: <AlignLeft size={18} /> },
  { type: 'number', label: 'Number', icon: <Hash size={18} /> },
  { type: 'email', label: 'Email', icon: <Mail size={18} /> },
  { type: 'select', label: 'Dropdown', icon: <ChevronDown size={18} /> },
  { type: 'checkbox', label: 'Checkboxes', icon: <CheckSquare size={18} /> },
  { type: 'radio', label: 'Multiple Choice', icon: <CircleDot size={18} /> },
  { type: 'date', label: 'Date', icon: <Calendar size={18} /> },
];

export const Sidebar = () => {
  const { addField, activePageId } = useFormContext();

  return (
    <div className="w-64 bg-white border-r border-gray-200 overflow-y-auto flex flex-col z-10 shadow-[4px_0_24px_rgba(0,0,0,0.02)]">
      <div className="p-4 border-b border-gray-100">
        <h2 className="text-sm font-bold text-gray-800 uppercase tracking-wider">Form Elements</h2>
        <p className="text-xs text-gray-500 mt-1">Click to add to form</p>
      </div>
      <div className="p-3 grid gap-2">
        {fieldTypes.map((field) => (
          <button
            key={field.type}
            onClick={() => activePageId && addField(activePageId, field.type)}
            className="flex items-center gap-3 p-3 rounded-xl border border-gray-100 hover:border-primary-200 hover:bg-primary-50 text-gray-700 hover:text-primary-700 transition-all duration-200 text-left shadow-sm hover:shadow"
          >
            <div className="text-primary-500">{field.icon}</div>
            <span className="font-medium text-sm">{field.label}</span>
          </button>
        ))}
      </div>
    </div>
  );
};
