import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export const useAuthStore = create(
  persist(
    (set) => ({
      user: null,
      accessToken: null,
      
      setAuth: (user, accessToken) => set({ user, accessToken }),
      
      logout: () => {
        set({ user: null, accessToken: null });
        // Optional: you can clear other things from localStorage here if needed
      },
    }),
    {
      name: 'erp-auth', // unique name for localStorage key
    }
  )
);
