import React from 'react';
import { Link } from 'react-router-dom';
import { MapPin, Users, ArrowRight } from 'lucide-react';
import { jobs } from '../data/mockData';

const JobListing = () => {
  const activeJobs = jobs.filter(job => job.is_active);

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="text-center space-y-4 py-12">
        <h1 className="text-4xl md:text-5xl font-extrabold text-slate-900 tracking-tight">
          Join our <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-500 to-teal-400">mission</span>
        </h1>
        <p className="text-lg text-slate-500 max-w-2xl mx-auto">
          We're looking for passionate individuals to help us build the future. 
          Explore our open roles below and find your perfect fit.
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {activeJobs.map(job => (
          <div key={job.id} className="bg-white rounded-2xl p-6 shadow-sm border border-slate-100 hover:shadow-xl hover:-translate-y-1 transition-all duration-300 group">
            <div className="flex justify-between items-start mb-4">
              <h2 className="text-2xl font-bold text-slate-800 group-hover:text-brand-600 transition-colors">
                {job.title}
              </h2>
              <span className="bg-brand-50 text-brand-700 text-xs font-semibold px-3 py-1 rounded-full whitespace-nowrap">
                {job.openings_count} Openings
              </span>
            </div>
            
            <p className="text-slate-600 mb-6 line-clamp-2">
              {job.description}
            </p>
            
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mt-auto">
              <div className="flex items-center gap-4 text-sm text-slate-500">
                <div className="flex items-center gap-1">
                  <MapPin size={16} />
                  <span>{job.location}</span>
                </div>
              </div>
              <Link 
                to={`/apply/${job.id}`} 
                className="inline-flex items-center justify-center gap-2 bg-slate-900 text-white px-5 py-2.5 rounded-xl font-medium hover:bg-brand-600 hover:shadow-lg hover:shadow-brand-500/30 transition-all focus:ring-4 focus:ring-brand-500/20 active:scale-95"
              >
                Apply Now
                <ArrowRight size={18} />
              </Link>
            </div>
          </div>
        ))}
      </div>
      
      {activeJobs.length === 0 && (
        <div className="text-center py-16 bg-white rounded-2xl border border-dashed border-slate-300">
          <Users size={48} className="mx-auto text-slate-300 mb-4" />
          <h3 className="text-xl font-bold text-slate-700">No open roles currently</h3>
          <p className="text-slate-500 mt-2">Check back later for new opportunities.</p>
        </div>
      )}
    </div>
  );
};

export default JobListing;
