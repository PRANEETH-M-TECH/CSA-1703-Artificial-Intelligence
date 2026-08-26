import { createContext, useContext, useEffect, useState, useCallback } from "react";
import { AuthAPI } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const loadUser = useCallback(async () => {
    const token = localStorage.getItem("taskmind_token");
    if (!token) {
      setLoading(false);
      return;
    }
    try {
      const me = await AuthAPI.me();
      setUser(me);
    } catch {
      localStorage.removeItem("taskmind_token");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadUser();
  }, [loadUser]);

  const login = async (email, password) => {
    const { access_token } = await AuthAPI.login({ email, password });
    localStorage.setItem("taskmind_token", access_token);
    const me = await AuthAPI.me();
    setUser(me);
    return me;
  };

  const signup = async (name, email, password) => {
    const { access_token } = await AuthAPI.signup({ name, email, password });
    localStorage.setItem("taskmind_token", access_token);
    const me = await AuthAPI.me();
    setUser(me);
    return me;
  };

  const logout = () => {
    localStorage.removeItem("taskmind_token");
    setUser(null);
  };

  const refreshUser = async () => {
    const me = await AuthAPI.me();
    setUser(me);
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, signup, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
