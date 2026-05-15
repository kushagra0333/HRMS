import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { useNavigate, Link } from 'react-router-dom';

export default function Login() {
  const [isAdminMode, setIsAdminMode] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    try {
      const user = await login(username, password);
      if (isAdminMode && user.role !== 'admin') {
        setError('Unauthorized: You are not an admin');
        return;
      }
      if (!isAdminMode && user.role === 'admin') {
        // Allow admins to log in via user portal too, or force admin portal?
        // Let's just allow it for now but maybe redirect to a different dashboard?
        // The user said "Admin can log in as Admin", "User can log in as User".
      }
      navigate('/');
    } catch (err) {
      setError('Invalid credentials');
    }
  };

  return (
    <div className={`min-h-screen ${isAdminMode ? 'bg-slate-900' : 'bg-gray-100'} flex items-center justify-center p-4 transition-colors duration-500`}>
      <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-md">
        <div className="flex justify-center mb-6">
            <div className="bg-gray-100 p-1 rounded-lg flex">
                <button 
                    onClick={() => setIsAdminMode(false)}
                    className={`px-4 py-1.5 rounded-md text-sm font-bold transition-all ${!isAdminMode ? 'bg-white shadow-sm text-blue-600' : 'text-gray-500'}`}
                >
                    Employee Login
                </button>
                <button 
                    onClick={() => setIsAdminMode(true)}
                    className={`px-4 py-1.5 rounded-md text-sm font-bold transition-all ${isAdminMode ? 'bg-white shadow-sm text-indigo-600' : 'text-gray-500'}`}
                >
                    Admin Login
                </button>
            </div>
        </div>
        
        <h1 className="text-2xl font-bold mb-6 text-center text-gray-800">
            {isAdminMode ? 'Admin Portal' : 'Employee Portal'}
        </h1>
        
        {error && <p className="text-red-500 text-sm mb-4 text-center bg-red-50 p-2 rounded">{error}</p>}
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
            <input
              type="text"
              required
              className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input
              type="password"
              required
              className="w-full p-2 border rounded-lg focus:ring-2 focus:ring-blue-500 outline-none"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button
            type="submit"
            className={`w-full ${isAdminMode ? 'bg-indigo-600 hover:bg-indigo-700' : 'bg-blue-600 hover:bg-blue-700'} text-white py-2.5 rounded-lg font-bold transition-all shadow-sm`}
          >
            {isAdminMode ? 'Access Admin Panel' : 'Sign In'}
          </button>
        </form>
        <p className="mt-6 text-center text-sm text-gray-600">
          New here? <Link to="/register" className="text-blue-600 hover:underline font-medium">Create an account</Link>
        </p>
      </div>
    </div>
  );
}
