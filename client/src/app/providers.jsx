import React, {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from 'react';

import {
  getCurrentUser,
  loginUser,
  registerUser,
} from '../services/api';

import {
  clearToken,
  getToken,
  setToken,
} from '../utils/storage';

const AuthContext = createContext(null);

export function AppProviders({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const refreshUser = useCallback(async () => {
    if (!getToken()) {
      setUser(null);
      return null;
    }

    const currentUser = await getCurrentUser();
    setUser(currentUser);
    return currentUser;
  }, []);

  useEffect(() => {
    let active = true;

    async function initializeAuth() {
      try {
        if (getToken()) {
          const currentUser = await getCurrentUser();
          if (active) setUser(currentUser);
        }
      } catch {
        clearToken();
        if (active) setUser(null);
      } finally {
        if (active) setLoading(false);
      }
    }

    initializeAuth();
    return () => { active = false; };
  }, []);

  const login = useCallback(async (email, password) => {
    const result = await loginUser(email, password);
    setToken(result.access_token);

    try {
      const currentUser = await getCurrentUser();
      setUser(currentUser);
      return currentUser;
    } catch (error) {
      clearToken();
      setUser(null);
      throw error;
    }
  }, []);

  const register = useCallback(
    (email, password) => registerUser(email, password),
    [],
  );

  const logout = useCallback(() => {
    clearToken();
    setUser(null);
  }, []);

  const value = {
    user,
    loading,
    isAuthenticated: Boolean(user),
    login,
    register,
    logout,
    refreshUser,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error('useAuth must be used inside AppProviders');
  }

  return context;
}

export default AppProviders;
