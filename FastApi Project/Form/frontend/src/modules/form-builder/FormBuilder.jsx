import { Sidebar } from './components/Sidebar';
import { Canvas } from './components/Canvas';
import { PropertiesPanel } from './components/PropertiesPanel';
import { useFormContext } from '../../context/FormContext';
import { FileText, Eye, Send } from 'lucide-react';

export const FormBuilder = () => {
  const { title, setTitle } = useFormContext();

  return (
    <div className="flex flex-col h-screen bg-googleBg overflow-hidden font-sans">
      {/* Top Toolbar - Google Forms Style */}
      <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6 shadow-sm z-20">
        <div className="flex items-center gap-4">
          <div className="w-10 h-10 bg-primary-100 rounded flex items-center justify-center text-primary-600">
            <FileText size={24} />
          </div>
          <input 
            type="text" 
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="text-lg text-gray-800 border-b border-transparent hover:border-gray-300 focus:outline-none focus:border-primary-600 px-1 py-1 transition-colors w-64"
          />
        </div>
        <div className="flex gap-4 items-center">
          <button className="p-2 text-gray-600 hover:bg-gray-100 rounded-full transition-colors" title="Preview">
            <Eye size={20} />
          </button>
          <button className="btn-primary flex items-center gap-2 px-5 py-2">
            <Send size={16} />
            <span>Send</span>
          </button>
        </div>
      </header>

      {/* Main Builder Area */}
      <div className="flex flex-1 overflow-hidden">
        {/* Left Sidebar - Field List */}
        <Sidebar />

        {/* Center - Builder Canvas */}
        <Canvas />

        {/* Right Sidebar - Properties Panel */}
        <PropertiesPanel />
      </div>
    </div>
  );
};
