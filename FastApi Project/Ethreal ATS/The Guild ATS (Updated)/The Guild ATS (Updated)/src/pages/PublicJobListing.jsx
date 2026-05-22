import React, { useState, useEffect } from 'react';
import { Link } from 'react-router';
import { Briefcase, MapPin, Clock, ArrowRight } from 'lucide-react';

export default function PublicJobListing() {
  const [jobs, setJobs] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  // Mock fetching from backend (JobRequisitionRecord)
  useEffect(() => {
    // Ideally this hits GET /entity/job_requisition/records
    setTimeout(() => {
      setJobs([
        { id: '1', title: 'Senior React Developer', location: 'Remote', type: 'Full-time', department: 'Engineering' },
        { id: '2', title: 'Product Designer', location: 'New York, NY', type: 'Full-time', department: 'Design' },
        { id: '3', title: 'DevOps Engineer', location: 'London, UK', type: 'Contract', department: 'Infrastructure' },
      ]);
      setIsLoading(false);
    }, 800);
  }, []);

  return (
    <div className="min-h-screen bg-background text-foreground relative overflow-hidden">
      {/* Background Gradients */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden -z-10">
        <div className="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] rounded-full bg-blue-500/10 blur-[120px]" />
        <div className="absolute top-[60%] -right-[10%] w-[30%] h-[40%] rounded-full bg-purple-500/10 blur-[120px]" />
      </div>

      <header className="border-b border-white/10 bg-white/5 backdrop-blur-md sticky top-0 z-20">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="bg-primary text-primary-foreground p-2 rounded-xl shadow-lg shadow-primary/20">
              <Briefcase size={24} />
            </div>
            <h1 className="text-2xl font-bold tracking-tight">Aerospace ERP</h1>
          </div>
          <Link to="/admin" className="text-sm font-medium hover:text-primary transition-colors">
            Employee Login
          </Link>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-16">
        <div className="text-center mb-16 animate-slide-up">
          <h2 className="text-5xl font-extrabold tracking-tight mb-4">Join Our Mission</h2>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Help us build the next generation of aerospace technology. Explore our open positions below.
          </p>
        </div>

        {isLoading ? (
          <div className="flex justify-center items-center h-40">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {jobs.map((job) => (
              <div 
                key={job.id} 
                className="group bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6 hover:bg-white/10 transition-all duration-300 hover:shadow-xl hover:shadow-primary/5 hover:-translate-y-1"
              >
                <div className="inline-flex items-center rounded-full border border-primary/20 bg-primary/10 px-2.5 py-0.5 text-xs font-semibold text-primary mb-4">
                  {job.department}
                </div>
                <h3 className="text-xl font-bold mb-2 group-hover:text-primary transition-colors">{job.title}</h3>
                <div className="flex flex-col gap-2 text-sm text-muted-foreground mb-6">
                  <span className="flex items-center gap-2"><MapPin size={16} /> {job.location}</span>
                  <span className="flex items-center gap-2"><Clock size={16} /> {job.type}</span>
                </div>
                <Link 
                  to={`/apply/${job.id}`}
                  className="inline-flex items-center justify-center gap-2 w-full bg-primary text-primary-foreground py-2.5 rounded-xl font-medium hover:bg-primary/90 transition-colors"
                >
                  Apply Now <ArrowRight size={16} />
                </Link>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
