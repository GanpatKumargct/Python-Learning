import React, { useState, useEffect } from 'react';
import { DragDropContext, Droppable, Draggable } from '@hello-pangea/dnd';
import { Mail, Phone, ExternalLink, Calendar, X, FileText, User } from 'lucide-react';
import { applications as initialApps, STAGES, jobs } from '../data/mockData';

const PipelineBoard = () => {
  const [columns, setColumns] = useState({});
  const [selectedApp, setSelectedApp] = useState(null);

  useEffect(() => {
    // Initialize columns from mock data
    const initialColumns = STAGES.reduce((acc, stage) => {
      acc[stage] = initialApps.filter(app => app.current_stage === stage);
      return acc;
    }, {});
    setColumns(initialColumns);
  }, []);

  const onDragEnd = (result) => {
    const { source, destination, draggableId } = result;

    if (!destination) return;
    if (source.droppableId === destination.droppableId && source.index === destination.index) return;

    const sourceCol = [...columns[source.droppableId]];
    const destCol = [...columns[destination.droppableId]];
    const [movedItem] = sourceCol.splice(source.index, 1);

    movedItem.current_stage = destination.droppableId;
    
    // Add to history
    movedItem.history.push({
      stage: destination.droppableId,
      date: new Date().toISOString().split('T')[0]
    });

    destCol.splice(destination.index, 0, movedItem);

    setColumns({
      ...columns,
      [source.droppableId]: sourceCol,
      [destination.droppableId]: destCol,
    });
  };

  const getJobTitle = (jobId) => {
    return jobs.find(j => j.id === jobId)?.title || 'Unknown Role';
  };

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col animate-in fade-in duration-500">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-800">Pipeline Board</h1>
        <p className="text-slate-500">Drag and drop candidates to update their stage.</p>
      </div>

      <div className="flex-1 overflow-hidden pb-4">
        <DragDropContext onDragEnd={onDragEnd}>
          <div className="grid grid-cols-4 gap-6 h-full">
            {STAGES.map(stage => (
              <div key={stage} className="flex flex-col h-full overflow-hidden bg-slate-200/50 rounded-2xl">
                <div className="p-4 flex items-center justify-between border-b border-slate-200/50">
                  <h3 className="font-bold text-slate-700">{stage}</h3>
                  <span className="bg-slate-200 text-slate-600 text-xs font-bold px-2.5 py-1 rounded-full">
                    {columns[stage]?.length || 0}
                  </span>
                </div>
                
                <Droppable droppableId={stage}>
                  {(provided, snapshot) => (
                    <div
                      {...provided.droppableProps}
                      ref={provided.innerRef}
                      className={`flex-1 p-3 overflow-y-auto space-y-3 transition-colors ${
                        snapshot.isDraggingOver ? 'bg-slate-200/80' : ''
                      }`}
                    >
                      {columns[stage]?.map((app, index) => (
                        <Draggable key={app.id} draggableId={app.id} index={index}>
                          {(provided, snapshot) => (
                            <div
                              ref={provided.innerRef}
                              {...provided.draggableProps}
                              {...provided.dragHandleProps}
                              onClick={() => setSelectedApp(app)}
                              className={`bg-slate-900 p-4 rounded-xl shadow-sm border border-slate-700 cursor-pointer hover:border-slate-500 transition-all ${
                                snapshot.isDragging ? 'shadow-lg ring-2 ring-slate-500 ring-opacity-50 rotate-2 scale-105' : ''
                              }`}
                            >
                              <h4 className="font-bold text-white">{app.full_name}</h4>
                              <p className="text-xs text-slate-400 font-medium mb-3">{getJobTitle(app.job_id)}</p>
                              
                              <div className="flex flex-wrap gap-1 mt-2">
                                {app.skills.slice(0, 3).map(skill => (
                                  <span key={skill} className="text-[10px] bg-slate-800 text-slate-300 border border-slate-700 px-2 py-0.5 rounded-full">
                                    {skill}
                                  </span>
                                ))}
                                {app.skills.length > 3 && (
                                  <span className="text-[10px] bg-slate-800 text-slate-300 border border-slate-700 px-2 py-0.5 rounded-full">
                                    +{app.skills.length - 3}
                                  </span>
                                )}
                              </div>
                            </div>
                          )}
                        </Draggable>
                      ))}
                      {provided.placeholder}
                    </div>
                  )}
                </Droppable>
              </div>
            ))}
          </div>
        </DragDropContext>
      </div>

      {/* Candidate Detail Modal */}
      {selectedApp && (
        <div className="fixed inset-0 z-50 flex justify-end bg-slate-900/20 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="w-full max-w-md bg-white h-full shadow-2xl flex flex-col animate-in slide-in-from-right duration-300 border-l border-slate-200">
            <div className="p-6 border-b border-slate-100 flex justify-between items-start bg-slate-50">
              <div>
                <h2 className="text-2xl font-bold text-slate-800">{selectedApp.full_name}</h2>
                <p className="text-brand-600 font-medium">{getJobTitle(selectedApp.job_id)}</p>
                <div className="inline-block mt-2 bg-slate-200 text-slate-700 text-xs font-bold px-3 py-1 rounded-full">
                  Stage: {selectedApp.current_stage}
                </div>
              </div>
              <button 
                onClick={() => setSelectedApp(null)}
                className="p-2 hover:bg-slate-200 rounded-full text-slate-500 transition-colors"
              >
                <X size={20} />
              </button>
            </div>
            
            <div className="flex-1 overflow-y-auto p-6 space-y-8">
              {/* Contact Info */}
              <section>
                <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4 flex items-center gap-2">
                  <User size={14} /> Contact Details
                </h3>
                <div className="space-y-3">
                  <a href={`mailto:${selectedApp.email}`} className="flex items-center gap-3 text-slate-600 hover:text-brand-600 transition-colors group">
                    <div className="p-2 bg-slate-100 rounded-lg group-hover:bg-brand-50"><Mail size={16} /></div>
                    {selectedApp.email}
                  </a>
                  <a href={`tel:${selectedApp.phone}`} className="flex items-center gap-3 text-slate-600 hover:text-brand-600 transition-colors group">
                    <div className="p-2 bg-slate-100 rounded-lg group-hover:bg-brand-50"><Phone size={16} /></div>
                    {selectedApp.phone}
                  </a>
                  <a href={selectedApp.resume_link} target="_blank" rel="noreferrer" className="flex items-center gap-3 text-slate-600 hover:text-brand-600 transition-colors group mt-4">
                    <div className="p-2 bg-slate-100 rounded-lg group-hover:bg-brand-50"><FileText size={16} /></div>
                    <span className="flex items-center gap-1 font-medium">View Resume <ExternalLink size={14} /></span>
                  </a>
                </div>
              </section>

              {/* Extracted Data */}
              <section>
                <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4">Extracted Intelligence</h3>
                <div className="bg-brand-50 rounded-xl p-4 border border-brand-100">
                  <div className="mb-4">
                    <p className="text-sm text-slate-500 mb-1">Education</p>
                    <p className="font-medium text-slate-800">{selectedApp.education}</p>
                  </div>
                  <div>
                    <p className="text-sm text-slate-500 mb-2">Top Skills</p>
                    <div className="flex flex-wrap gap-2">
                      {selectedApp.skills.map(skill => (
                        <span key={skill} className="bg-white border border-brand-200 text-brand-700 text-xs px-2.5 py-1 rounded-md font-medium">
                          {skill}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </section>

              {/* Timeline */}
              <section>
                <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4 flex items-center gap-2">
                  <Calendar size={14} /> Application History
                </h3>
                <div className="relative border-l-2 border-slate-100 ml-3 space-y-6">
                  {selectedApp.history.map((hist, idx) => (
                    <div key={idx} className="relative pl-6">
                      <div className="absolute w-3 h-3 bg-brand-500 rounded-full -left-[7px] top-1.5 ring-4 ring-white"></div>
                      <p className="font-bold text-slate-700">{hist.stage}</p>
                      <p className="text-xs text-slate-500 mt-1">Moved on {hist.date}</p>
                    </div>
                  ))}
                </div>
              </section>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PipelineBoard;
