import React, { useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { ArrowLeft, CheckCircle2, UploadCloud } from 'lucide-react';
import { jobs } from '../data/mockData';

const ApplicationForm = () => {
  const { jobId } = useParams();
  const job = jobs.find(j => j.id === jobId);
  
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    resumeLink: ''
  });
  const [submitted, setSubmitted] = useState(false);

  if (!job) {
    return <div className="text-center py-12 text-slate-500">Job not found.</div>;
  }

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Simulate API call
    setTimeout(() => {
      setSubmitted(true);
    }, 800);
  };

//   const handleSubmit = (e) => {
//   e.preventDefault(); // 1. Stop the page from refreshing

//   // 2. Call the backend API
//   // Replace 'http://localhost:5000/api/apply' with your actual backend link
//   fetch('http://localhost:5000/api/apply', {
//     method: 'POST', // We use POST because we are SENDING data
//     headers: {
//       'Content-Type': 'application/json', // Tell the backend we are sending JSON
//     },
//     body: JSON.stringify(formData), // Turn your form data into a string for the server
//   })
//     .then((response) => {
//       if (response.ok) {
//         // 3. If the backend says "OK", then show the success message
//         setSubmitted(true);
//       } else {
//         // Handle cases where the server is broken or data is wrong
//         alert("Something went wrong on the server.");
//       }
//     })
//     .catch((error) => {
//       // Handle cases where the internet is down or server is offline
//       console.error("Error:", error);
//       alert("Could not connect to the backend.");
//     });
// };


  if (submitted) {
    return (
      <div className="max-w-md mx-auto mt-12 bg-white rounded-2xl shadow-xl p-8 text-center border border-brand-100 animate-in zoom-in-95 duration-500">
        <div className="w-20 h-20 bg-brand-50 text-brand-500 rounded-full flex items-center justify-center mx-auto mb-6">
          <CheckCircle2 size={48} />
        </div>
        <h2 className="text-3xl font-bold text-slate-800 mb-2">Application Received!</h2>
        <p className="text-slate-500 mb-8">
          Thank you for applying to the <span className="font-semibold text-slate-700">{job.title}</span> position. We'll review your application and get back to you soon.
        </p>
        <Link 
          to="/" 
          className="inline-block bg-slate-100 text-slate-700 px-6 py-3 rounded-xl font-medium hover:bg-slate-200 transition-colors"
        >
          Return to Job Listings
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto animate-in fade-in duration-500">
      <Link to="/" className="inline-flex items-center gap-2 text-slate-500 hover:text-slate-800 mb-6 transition-colors">
        <ArrowLeft size={16} /> Back to roles
      </Link>
      
      <div className="bg-white rounded-3xl shadow-sm border border-slate-200 overflow-hidden">
        <div className="bg-slate-900 px-8 py-10 text-white">
          <h1 className="text-3xl font-bold mb-2">Apply for {job.title}</h1>
          <p className="text-slate-300 opacity-90 flex items-center gap-2">
            <span>{job.location}</span>
          </p>
        </div>

        <form onSubmit={handleSubmit} className="p-8 space-y-6">
          <div className="space-y-4">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-slate-700 mb-1">Full Name</label>
              <input 
                type="text" 
                id="name" 
                name="name" 
                required
                value={formData.name}
                onChange={handleChange}
                className="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none transition-all"
                placeholder="Jane Doe"
              />
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-slate-700 mb-1">Email Address</label>
                <input 
                  type="email" 
                  id="email" 
                  name="email" 
                  required
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none transition-all"
                  placeholder="jane@example.com"
                />
              </div>
              <div>
                <label htmlFor="phone" className="block text-sm font-medium text-slate-700 mb-1">Phone Number</label>
                <input 
                  type="tel" 
                  id="phone" 
                  name="phone" 
                  required
                  value={formData.phone}
                  onChange={handleChange}
                  className="w-full px-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none transition-all"
                  placeholder="+1 (555) 000-0000"
                />
              </div>
            </div>

            <div>
              <label htmlFor="resumeLink" className="block text-sm font-medium text-slate-700 mb-1">Resume Link (Google Drive, Dropbox, etc.)</label>
              <div className="relative">
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-slate-400">
                  <UploadCloud size={18} />
                </div>
                <input 
                  type="url" 
                  id="resumeLink" 
                  name="resumeLink" 
                  required
                  value={formData.resumeLink}
                  onChange={handleChange}
                  className="w-full pl-11 pr-4 py-3 rounded-xl border border-slate-300 focus:ring-2 focus:ring-brand-500 focus:border-brand-500 outline-none transition-all"
                  placeholder="https://drive.google.com/..."
                />
              </div>
              <p className="text-xs text-slate-500 mt-2">Please ensure the link is publicly accessible.</p>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-100">
            <button 
              type="submit" 
              className="w-full bg-brand-600 text-white py-3.5 rounded-xl font-bold hover:bg-brand-700 hover:shadow-lg hover:shadow-brand-500/20 active:scale-[0.98] transition-all"
            >
              Submit Application
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ApplicationForm;
