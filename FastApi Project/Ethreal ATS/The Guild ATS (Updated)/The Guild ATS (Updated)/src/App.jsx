import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router";
import { AdminDashboard } from "@/pages/AdminDashboard";
import PublicJobListing from "@/pages/PublicJobListing";
import PublicApplicationForm from "@/pages/PublicApplicationForm";

function App() {
  return (
    <Router>
      <Routes>
        {/* Public Candidate Routes */}
        <Route path="/" element={<PublicJobListing />} />
        <Route path="/apply/:jobId" element={<PublicApplicationForm />} />

        {/* Private HR/Admin Routes */}
        <Route path="/admin/*" element={<AdminDashboard />} />
        
        {/* Redirect unknown routes */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
