import { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for token in localStorage and validate/load user
    const token = localStorage.getItem('access_token');
    if (token) {
        // We decode token or fetch user profile. 
        // For simplicity, let's assume we store user info or fetch it.
        // Let's retry fetching user profile? Or just set loggedIn state. 
        // Ideally we have a /api/auth/me/ endpoint. I haven't created one.
        // I'll decoding the JWT token to get username/id if needed, or just persist user object.
        const storedUser = localStorage.getItem('user_data');
        if (storedUser) {
            setUser(JSON.parse(storedUser));
        }
    }
    setLoading(false);
  }, []);

  const login = async (username, password) => {
    const response = await api.post('/token/', { username, password });
    const { access, refresh } = response.data;
    
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    
    // Decode token or minimal user info?
    // Let's assume response includes user info or we decode it.
    // Standard SimpleJWT doesn't return user info.
    // I should probably fetch it or modifying settings to return it.
    // OR create a /me endpoint.
    
    // For now, let's just create a basic user object from username.
    const userData = { username }; // Placeholder until we have /me
    setUser(userData);
    localStorage.setItem('user_data', JSON.stringify(userData));
    
    // Set default header
    api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
    return true;
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
