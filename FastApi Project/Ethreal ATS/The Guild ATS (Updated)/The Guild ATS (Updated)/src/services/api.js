import { departments } from '@/features/ats/data/Departments';

const API_BASE_URL = "http://localhost:8000";
// For Phase 1, we simulate an admin token. In reality, Zoho SSO provides this.
const dummyAuthHeader = {
  "Authorization": "Bearer admin_token_placeholder"
};

export const getDepartments = async () => {
  // We can keep departments static or fetch them if an endpoint exists.
  // For now, relying on static data as the backend only models entities.
  return departments;
};

export const getCandidates = async () => {
  try {
    const res = await fetch(`${API_BASE_URL}/entity/candidate/records`, {
      headers: dummyAuthHeader
    });
    if (!res.ok) throw new Error("Failed to fetch candidates");
    const records = await res.json();
    
    // Transform backend generic record format to UI format
    return records.map(r => ({
      id: r.id,
      ...r.data
    }));
  } catch (e) {
    console.error(e);
    return [];
  }
};

export const updateCandidateStatus = async (candidateId, status) => {
  try {
    const res = await fetch(`${API_BASE_URL}/workflow/transition`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...dummyAuthHeader
      },
      body: JSON.stringify({
        instance_id: candidateId, // Assuming instance_id corresponds roughly to record_id in this context for Phase 1
        transition_name: `move_to_${status}`, // Naive mapping
        payload: { status },
        idempotency_key: `trans_${candidateId}_${status}_${Date.now()}`
      })
    });
    
    if (!res.ok) throw new Error("Failed to transition");
    return { success: true, candidateId, status };
  } catch (e) {
    console.error(e);
    throw e;
  }
};
