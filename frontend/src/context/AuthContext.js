import { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
        api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
        fetchUser();
    } else {
        setLoading(false);
    }
  }, []);

  const fetchUser = async () => {
    try {
        const response = await api.get('/me/');
        setUser(response.data);
        return response.data;
    } catch (error) {
        logout();
    } finally {
        setLoading(false);
    }
  };

  const login = async (username, password) => {
    const response = await api.post('/token/', { username, password });
    const { access, refresh } = response.data;
    
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    
    api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
    const userData = await fetchUser();
    return userData;
  };

  const register = async (userData) => {
    await api.post('/auth/register/', userData);
    return true;
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user_data');
    delete api.defaults.headers.common['Authorization'];
  };

  return (
    <AuthContext.Provider value={{ user, login, register, logout, loading }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};
