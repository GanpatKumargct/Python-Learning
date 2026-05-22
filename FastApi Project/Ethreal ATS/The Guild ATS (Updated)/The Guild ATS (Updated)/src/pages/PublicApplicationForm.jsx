import React, { useState } from 'react';
import { useParams, Link } from 'react-router';
import { ArrowLeft, CheckCircle2, UploadCloud, Briefcase } from 'lucide-react';

export default function PublicApplicationForm() {
  const { jobId } = useParams();
  
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    resumeLink: ''
  });
  const [submitted, setSubmitted] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    
    try {
      const response = await fetch('http://localhost:8000/entity/candidate/records', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          data: {
            ...formData,
            jobId: jobId,
            status: 'applied'
          }
        }),
      });
      
      if (response.ok) {
        setSubmitted(true);
      } else {
        alert("Something went wrong on the server.");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("Could not connect to the backend.");
    } finally {
      setIsSubmitting(false);
    }
  };

  if (submitted) {
    return (
      <div className="min-h-screen bg-background text-foreground flex items-center justify-center p-6 relative overflow-hidden">
        <div className="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] rounded-full bg-blue-500/10 blur-[120px]" />
        
        <div className="max-w-md w-full bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl shadow-2xl p-8 text-center animate-zoom-in">
          <div className="w-20 h-20 bg-green-500/20 text-green-500 rounded-full flex items-center justify-center mx-auto mb-6 shadow-[0_0_40px_rgba(34,197,94,0.3)]">
            <CheckCircle2 size={40} />
          </div>
          <h2 className="text-3xl font-bold mb-2">Application Received!</h2>
          <p className="text-muted-foreground mb-8">
            Thank you for applying. Our team will review your application and get back to you shortly.
          </p>
          <Link 
            to="/" 
            className="inline-block bg-primary text-primary-foreground px-6 py-3 rounded-xl font-medium hover:bg-primary/90 transition-colors"
          >
            Return to Job Listings
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background text-foreground relative overflow-hidden">
      <div className="absolute top-[60%] -right-[10%] w-[30%] h-[40%] rounded-full bg-purple-500/10 blur-[120px]" />
      
      <div className="max-w-2xl mx-auto px-6 py-12 animate-fade-in">
        <Link to="/" className="inline-flex items-center gap-2 text-muted-foreground hover:text-foreground mb-8 transition-colors">
          <ArrowLeft size={16} /> Back to roles
        </Link>
        
        <div className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl shadow-2xl overflow-hidden relative">
          <div className="bg-primary/10 px-8 py-10 border-b border-white/10">
            <h1 className="text-3xl font-bold mb-2">Submit Your Application</h1>
            <p className="text-muted-foreground flex items-center gap-2">
              <Briefcase size={16}/> Job ID: {jobId}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="p-8 space-y-6">
            <div className="space-y-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium mb-1.5">Full Name</label>
                <input 
                  type="text" id="name" name="name" required
                  value={formData.name} onChange={handleChange}
                  className="w-full px-4 py-3 bg-black/20 border border-white/10 rounded-xl focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all placeholder:text-white/20"
                  placeholder="Jane Doe"
                />
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label htmlFor="email" className="block text-sm font-medium mb-1.5">Email Address</label>
                  <input 
                    type="email" id="email" name="email" required
                    value={formData.email} onChange={handleChange}
                    className="w-full px-4 py-3 bg-black/20 border border-white/10 rounded-xl focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all placeholder:text-white/20"
                    placeholder="jane@example.com"
                  />
                </div>
                <div>
                  <label htmlFor="phone" className="block text-sm font-medium mb-1.5">Phone Number</label>
                  <input 
                    type="tel" id="phone" name="phone" required
                    value={formData.phone} onChange={handleChange}
                    className="w-full px-4 py-3 bg-black/20 border border-white/10 rounded-xl focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all placeholder:text-white/20"
                    placeholder="+1 (555) 000-0000"
                  />
                </div>
              </div>

              <div>
                <label htmlFor="resumeLink" className="block text-sm font-medium mb-1.5">Resume Link (Drive, Dropbox, etc.)</label>
                <div className="relative">
                  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-muted-foreground">
                    <UploadCloud size={18} />
                  </div>
                  <input 
                    type="url" id="resumeLink" name="resumeLink" required
                    value={formData.resumeLink} onChange={handleChange}
                    className="w-full pl-11 pr-4 py-3 bg-black/20 border border-white/10 rounded-xl focus:ring-2 focus:ring-primary focus:border-primary outline-none transition-all placeholder:text-white/20"
                    placeholder="https://drive.google.com/..."
                  />
                </div>
              </div>
            </div>

            <div className="pt-6">
              <button 
                type="submit" 
                disabled={isSubmitting}
                className="w-full bg-primary text-primary-foreground py-3.5 rounded-xl font-bold hover:bg-primary/90 hover:shadow-lg hover:shadow-primary/20 active:scale-[0.98] transition-all flex items-center justify-center disabled:opacity-70 disabled:cursor-not-allowed"
              >
                {isSubmitting ? (
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                ) : (
                  "Submit Application"
                )}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
