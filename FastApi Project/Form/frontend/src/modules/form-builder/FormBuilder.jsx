import { Sidebar } from './components/Sidebar';
import { Canvas } from './components/Canvas';
import { PropertiesPanel } from './components/PropertiesPanel';
import { useFormContext } from '../../context/FormContext';

export const FormBuilder = () => {
  const { title, setTitle } = useFormContext();

  return (
    <div className="flex flex-col h-screen bg-gray-50 overflow-hidden">
      {/* Top Toolbar */}
      <header className="h-16 bg-white border-b border-gray-200 flex items-center justify-between px-6 shadow-sm z-10">
        <div className="flex items-center gap-4">
          <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center text-white font-bold">F</div>
          <input 
            type="text" 
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="text-xl font-semibold bg-transparent border-none focus:outline-none focus:ring-2 focus:ring-primary-500 rounded px-2"
          />
        </div>
        <div className="flex gap-3">
          <button className="btn-secondary">Preview</button>
          <button className="btn-primary">Publish Form</button>
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
