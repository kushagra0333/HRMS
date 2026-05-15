import { useEffect, useState } from "react";
import api, { endpoints } from "../services/api";
import { CalendarCheck, CheckCircle, XCircle } from "lucide-react";
import { useAuth } from "../context/AuthContext";

export default function Attendance() {
  const [attendance, setAttendance] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [formData, setFormData] = useState({
    employee: "", // Employee ID slug
    date: new Date().toISOString().split("T")[0],
    status: "Present",
  });

  const { user } = useAuth();
  const isAdmin = user?.role === 'admin';

  const fetchData = async () => {
    try {
      const [attRes, empRes] = await Promise.all([
        api.get(endpoints.attendance),
        isAdmin ? api.get(endpoints.employees) : Promise.resolve({ data: [] }),
      ]);
      setAttendance(attRes.data);
      setEmployees(empRes.data);
    } catch (error) {
      console.error("Failed to fetch data", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, [isAdmin]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // If admin doesn't select an employee, treat it as a self-check-in
      const payload = (isAdmin && formData.employee) 
        ? formData 
        : { date: formData.date, status: formData.status };
      
      await api.post(endpoints.attendance, payload);
      alert("Attendance marked successfully!");
      fetchData();
    } catch (error) {
      console.error("Attendance Error:", error.response?.data);
      const errorMsg = error.response?.data 
        ? (typeof error.response.data === 'string' ? error.response.data : JSON.stringify(error.response.data))
        : error.message;
      alert("Failed to mark attendance: " + errorMsg);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Attendance</h1>
          <p className="text-gray-500">{isAdmin ? 'Track company attendance' : 'Your attendance history'}</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Mark Attendance Form */}
            <div className="bg-white p-6 rounded-xl shadow-sm border h-fit">
                <h2 className="text-lg font-bold mb-4 flex items-center gap-2 text-gray-800">
                    <CalendarCheck className="w-5 h-5 text-blue-600" />
                    {isAdmin ? 'Mark Attendance' : 'Self Check-in'}
                </h2>
                <form onSubmit={handleSubmit} className="space-y-4">
                    {isAdmin && (
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">Employee</label>
                            <select 
                                required
                                className="w-full p-2 border rounded-lg bg-white"
                                value={formData.employee}
                                onChange={(e) => setFormData({...formData, employee: e.target.value})}
                            >
                                <option value="">Select Employee</option>
                                {employees.map(emp => (
                                    <option key={emp.id} value={emp.employee_id}>
                                        {emp.name} ({emp.employee_id})
                                    </option>
                                ))}
                            </select>
                        </div>
                    )}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Date</label>
                        <input 
                            type="date" 
                            required
                            className="w-full p-2 border rounded-lg"
                            value={formData.date}
                            onChange={(e) => setFormData({...formData, date: e.target.value})}
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                        <div className="flex gap-4">
                            <label className="flex items-center gap-2 cursor-pointer">
                                <input 
                                    type="radio" 
                                    name="status" 
                                    value="Present"
                                    checked={formData.status === "Present"}
                                    onChange={(e) => setFormData({...formData, status: e.target.value})}
                                    className="text-blue-600"
                                />
                                Present
                            </label>
                            <label className="flex items-center gap-2 cursor-pointer">
                                <input 
                                    type="radio" 
                                    name="status" 
                                    value="Absent"
                                    checked={formData.status === "Absent"}
                                    onChange={(e) => setFormData({...formData, status: e.target.value})}
                                    className="text-red-600"
                                />
                                Absent
                            </label>
                        </div>
                    </div>
                    <button type="submit" className="w-full py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium border-t pt-4 mt-6">
                        Submit
                    </button>
                </form>
            </div>

            {/* Attendance History */}
            <div className="md:col-span-2 bg-white rounded-xl shadow-sm border overflow-hidden">
                <div className="p-4 border-b">
                    <h2 className="text-lg font-bold">Recent Records</h2>
                </div>
                <div className="overflow-x-auto">
                <table className="w-full text-left text-sm text-gray-600">
                    <thead className="bg-gray-50 border-b text-xs uppercase font-medium text-gray-500">
                        <tr>
                            <th className="px-6 py-3">Date</th>
                            <th className="px-6 py-3">Employee</th>
                            <th className="px-6 py-3">Status</th>
                        </tr>
                    </thead>
                    <tbody className="divide-y">
                        {loading ? (
                             <tr><td colSpan="3" className="p-6 text-center">Loading...</td></tr>
                        ) : attendance.length === 0 ? (
                            <tr><td colSpan="3" className="p-6 text-center">No records found.</td></tr>
                        ) : (
                            attendance.map((record) => {
                                const empName = record.employee_name || record.employee;
                                
                                return (
                                    <tr key={record.id} className="hover:bg-gray-50">
                                        <td className="px-6 py-4">{record.date}</td>
                                        <td className="px-6 py-4 font-medium text-gray-900">{empName}</td>
                                        <td className="px-6 py-4">
                                            {record.status === 'Present' ? (
                                                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                                                    <CheckCircle className="w-3 h-3" /> Present
                                                </span>
                                            ) : (
                                                <span className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
                                                    <XCircle className="w-3 h-3" /> Absent
                                                </span>
                                            )}
                                        </td>
                                    </tr>
                                )
                            })
                        )}
                    </tbody>
                </table>
                </div>
            </div>
      </div>
    </div>
  );
}
