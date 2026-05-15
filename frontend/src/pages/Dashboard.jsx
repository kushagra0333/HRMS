import { useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { 
  Users, Briefcase, CheckCircle2, Clock, 
  AlertCircle, TrendingUp, Activity, ArrowRight 
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, 
  Tooltip, ResponsiveContainer, PieChart, Pie, Cell 
} from 'recharts';
import { Link } from 'react-router-dom';

export default function Dashboard() {
  const { user } = useAuth();
  const [stats, setStats] = useState({
    totalProjects: 0,
    totalUsers: 0,
    tasks: {
      pending: 0,
      in_progress: 0,
      completed: 0,
      overdue: 0,
      total: 0
    },
    recentTasks: []
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [projectsRes, tasksRes, employeesRes] = await Promise.all([
        api.get('/projects/'),
        api.get('/tasks/'),
        api.get('/employees/')
      ]);

      const tasks = tasksRes.data;
      const tasksStats = {
        pending: tasks.filter(t => t.status === 'pending').length,
        in_progress: tasks.filter(t => t.status === 'in_progress').length,
        completed: tasks.filter(t => t.status === 'completed').length,
        overdue: tasks.filter(t => t.status === 'overdue').length,
        total: tasks.length
      };

      setStats({
        totalProjects: projectsRes.data.length,
        totalUsers: employeesRes.data.length,
        tasks: tasksStats,
        recentTasks: tasks.slice(0, 5)
      });
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const chartData = [
    { name: 'Pending', value: stats.tasks.pending, color: '#f59e0b' },
    { name: 'In Progress', value: stats.tasks.in_progress, color: '#3b82f6' },
    { name: 'Completed', value: stats.tasks.completed, color: '#10b981' },
    { name: 'Overdue', value: stats.tasks.overdue, color: '#ef4444' },
  ];

  if (loading) return <div className="flex justify-center items-center h-full">Loading Dashboard...</div>;

  return (
    <div className="space-y-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Welcome back, {user?.username}!</h1>
          <p className="text-gray-500">Here's what's happening in your workspace today.</p>
        </div>
        <div className="flex items-center gap-2 bg-white px-4 py-2 rounded-xl shadow-sm border border-gray-100">
          <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse" />
          <span className="text-sm font-medium text-gray-700">System Live</span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard icon={<Briefcase />} label="Total Projects" value={stats.totalProjects} color="blue" />
        {user?.role === 'admin' && <StatCard icon={<Users />} label="Total Users" value={stats.totalUsers} color="indigo" />}
        <StatCard icon={<CheckCircle2 />} label="Completed Tasks" value={stats.tasks.completed} color="green" />
        <StatCard icon={<AlertCircle />} label="Overdue Tasks" value={stats.tasks.overdue} color="red" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Analytics Chart */}
        <div className="lg:col-span-2 bg-white p-6 rounded-2xl border border-gray-100 shadow-sm space-y-6">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-bold text-gray-800">Tasks Overview</h3>
            <Activity className="w-5 h-5 text-gray-400" />
          </div>
          <div className="h-80 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f3f4f6" />
                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{fill: '#6b7280', fontSize: 12}} />
                <YAxis axisLine={false} tickLine={false} tick={{fill: '#6b7280', fontSize: 12}} />
                <Tooltip 
                  cursor={{fill: '#f9fafb'}}
                  contentStyle={{borderRadius: '12px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)'}}
                />
                <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Recent Activity / Tasks */}
        <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm space-y-6">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-bold text-gray-800">Recent Tasks</h3>
            <Link to="/tasks" className="text-sm text-indigo-600 font-medium flex items-center gap-1">
              View All <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
          <div className="space-y-4">
            {stats.recentTasks.map((task) => (
              <div key={task.id} className="flex items-center gap-4 p-3 rounded-xl hover:bg-gray-50 transition-colors group">
                <div className={`p-2 rounded-lg ${
                  task.status === 'completed' ? 'bg-green-50 text-green-600' : 
                  task.status === 'overdue' ? 'bg-red-50 text-red-600' : 'bg-gray-50 text-gray-400'
                }`}>
                  <TrendingUp className="w-4 h-4" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-bold text-gray-800 truncate">{task.title}</p>
                  <p className="text-xs text-gray-500 truncate">{task.project_title}</p>
                </div>
                <div className="text-right">
                  <span className="text-[10px] font-bold uppercase text-gray-400 group-hover:text-indigo-600 transition-colors">
                    {task.status.replace('_', ' ')}
                  </span>
                </div>
              </div>
            ))}
            {stats.recentTasks.length === 0 && (
              <p className="text-sm text-gray-500 text-center py-8 italic">No tasks found yet.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon, label, value, color }) {
  const colorMap = {
    blue: 'bg-blue-50 text-blue-600',
    indigo: 'bg-indigo-50 text-indigo-600',
    green: 'bg-green-50 text-green-600',
    red: 'bg-red-50 text-red-600',
  };

  return (
    <div className="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm space-y-4">
      <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${colorMap[color]}`}>
        {icon}
      </div>
      <div>
        <p className="text-sm font-medium text-gray-500">{label}</p>
        <p className="text-3xl font-bold text-gray-900">{value}</p>
      </div>
    </div>
  );
}
