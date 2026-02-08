import { useEffect, useState } from "react";
import api, { endpoints } from "../services/api";
import { Users, CalendarCheck, Clock, TrendingUp, CalendarDays } from "lucide-react";
import { useAuth } from "../context/AuthContext";

export default function Dashboard() {
    const { user } = useAuth();
    const [stats, setStats] = useState({
        totalEmployees: 0,
        presentToday: 0,
        absentToday: 0,
        pendingLeaves: 0,
        myAttendance: 0,
        myLeaves: 0,
    });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStats = async () => {
            try {
                // Determine if Admin or User
                // Simple logic: If we can fetch all employees, we show Admin stats.
                // Or we check specific permissions. For now, let's try to fetch everything and handle errors or empty data.
                
                const today = new Date().toISOString().split('T')[0];
                
                // Parallel fetch
                // If user is employee, /employees might fail or return only self? 
                // Actually my backend view for employees returns list. 
                // Permissions on EmployeeViewSet? Defaults to AllowAny? No, I didn't set it in views.py, so it defaults to AllowAny or IsAuthenticated depending on settings. 
                // Settings has DEFAULT_PERMISSION_CLASSES = IsAuthenticated.
                // So Employee can fetch list of employees? Usually yes in simple apps.
                
                const [empRes, attRes, leaveRes] = await Promise.all([
                    api.get(endpoints.employees),
                    api.get(endpoints.attendance),
                    api.get('/leaves/')
                ]);

                // Calculate stats
                const employees = empRes.data;
                const attendance = attRes.data;
                const leaves = leaveRes.data;
                
                const todaysAttendance = attendance.filter(a => a.date === today);
                
                // If user is "admin" (which we guess by... maybe checking a flag or just showing all data)
                // Actually, backend filters data for non-admin.
                // So `attendance` array will only contain MY attendance if I am not admin.
                // `leaves` array will only contain MY leaves.
                
                // So we can blindly calculate "total" from what we receive.
                // If I am admin, I receive all. If employee, I receive mine.
                
                setStats({
                    totalEmployees: employees.length,
                    presentToday: todaysAttendance.filter(a => a.status === 'Present').length,
                    absentToday: todaysAttendance.filter(a => a.status === 'Absent').length,
                    pendingLeaves: leaves.filter(l => l.status === 'Pending').length,
                    myAttendance: attendance.length, 
                    myLeaves: leaves.length
                });

            } catch (error) {
                console.error("Error fetching stats", error);
            } finally {
                setLoading(false);
            }
        };

        fetchStats();
    }, [user]);

    const adminCards = [
        { label: "Total Employees", value: stats.totalEmployees, icon: Users, color: "bg-blue-500" },
        { label: "Present Today", value: stats.presentToday, icon: CalendarCheck, color: "bg-green-500" },
        { label: "Pending Leaves", value: stats.pendingLeaves, icon: CalendarDays, color: "bg-orange-500" },
    ];

    const employeeCards = [
         { label: "My Attendance Days", value: stats.myAttendance, icon: CalendarCheck, color: "bg-blue-500" },
         { label: "My Leaves", value: stats.myLeaves, icon: CalendarDays, color: "bg-purple-500" },
         { label: "Status Today", value: stats.presentToday > 0 ? "Present" : "Not Marked", icon: Clock, color: stats.presentToday > 0 ? "bg-green-500" : "bg-gray-400" },
    ];
    
    // Heuristic to decide which cards to show:
    // If stats.totalEmployees > 1, likely Admin (or just seeing everyone).
    // Or we can try to guess from user.username or just show a mix?
    // Let's show "adminCards" by default, but maybe adapt labels?
    // Actually, if I am a normal employee, `totalEmployees` might be just 1 (myself) if filtered?
    // But EmployeeViewSet usually returns all.
    // Let's assume for now 
    // IF user username is 'admin' -> Show Admin Cards.
    // ELSE -> Show Employee Cards.
    
    const cards = user?.username === 'admin' ? adminCards : employeeCards;

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
            <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-gray-500">Welcome back, {user?.username}</p>
        </div>
        <div className="text-sm text-gray-500 bg-white px-4 py-2 rounded-lg border shadow-sm w-fit">
            {new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {cards.map((stat) => (
            <div key={stat.label} className="bg-white p-6 rounded-xl shadow-sm border flex items-center gap-4">
                <div className={`w-12 h-12 rounded-lg ${stat.color} text-white flex items-center justify-center`}>
                    <stat.icon className="w-6 h-6" />
                </div>
                <div>
                    <p className="text-sm text-gray-500">{stat.label}</p>
                    <p className="text-2xl font-bold text-gray-900">{stat.value}</p>
                </div>
            </div>
        ))}
      </div>

      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-2xl p-8 text-white shadow-lg">
        <div className="flex items-start justify-between">
            <div>
                <h2 className="text-2xl font-bold mb-2">HR Management Simplified</h2>
                <p className="text-blue-100 max-w-xl">
                    Manage your workforce efficiently with our streamlined tools for employee tracking and attendance management.
                </p>
            </div>
            <TrendingUp className="w-16 h-16 text-blue-400 opacity-50" />
        </div>
      </div>
    </div>
  );
}
