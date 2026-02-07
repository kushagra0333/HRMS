import { useEffect, useState } from "react";
import api from "../services/api";
import { Calendar, CheckCircle, XCircle, Clock } from "lucide-react";

export default function Leaves() {
  const [leaves, setLeaves] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    start_date: "",
    end_date: "",
    reason: "",
  });

  const fetchLeaves = async () => {
    try {
      const response = await api.get("/leaves/");
      setLeaves(response.data);
    } catch (error) {
      console.error("Failed to fetch leaves", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLeaves();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post("/leaves/", formData);
      setShowModal(false);
      setFormData({ start_date: "", end_date: "", reason: "" });
      fetchLeaves();
    } catch (error) {
        alert("Failed to apply for leave: " + (error.response?.data?.detail || error.message));
    }
  };

  const handleAction = async (id, action) => {
      try {
          await api.patch(`/leaves/${id}/${action}/`);
          fetchLeaves();
      } catch (error) {
          alert(`Failed to ${action} leave`);
      }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Leaves</h1>
          <p className="text-gray-500">Manage leave applications</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-lg flex items-center gap-2 hover:bg-blue-700 transition"
        >
          <Calendar className="w-4 h-4" />
          Apply for Leave
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
        <table className="w-full text-left text-sm text-gray-600">
          <thead className="bg-gray-50 border-b text-xs uppercase font-medium text-gray-500">
            <tr>
              <th className="px-6 py-3">Employee</th>
              <th className="px-6 py-3">Dates</th>
              <th className="px-6 py-3">Reason</th>
              <th className="px-6 py-3">Status</th>
              <th className="px-6 py-3">Applied On</th>
              {/* Admin Actions column? We'll conditionally render content if user is admin */}
              <th className="px-6 py-3 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {loading ? (
               <tr><td colSpan="6" className="p-6 text-center">Loading...</td></tr>
            ) : leaves.length === 0 ? (
                <tr><td colSpan="6" className="p-6 text-center">No leave records found.</td></tr>
            ) : (
              leaves.map((leave) => (
                <tr key={leave.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 font-medium text-gray-900">
                      {leave.employee_name || "Myself"} 
                      <span className="block text-xs text-gray-500">{leave.employee_id}</span>
                  </td>
                  <td className="px-6 py-4">
                    {leave.start_date} to {leave.end_date}
                  </td>
                  <td className="px-6 py-4 max-w-xs truncate" title={leave.reason}>
                      {leave.reason}
                  </td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        leave.status === 'Approved' ? 'bg-green-100 text-green-800' :
                        leave.status === 'Rejected' ? 'bg-red-100 text-red-800' :
                        'bg-yellow-100 text-yellow-800'
                    }`}>
                        {leave.status === 'Approved' && <CheckCircle className="w-3 h-3" />}
                        {leave.status === 'Rejected' && <XCircle className="w-3 h-3" />}
                        {leave.status === 'Pending' && <Clock className="w-3 h-3" />}
                        {leave.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-gray-500">{new Date(leave.applied_on).toLocaleDateString()}</td>
                  <td className="px-6 py-4 text-right space-x-2">
                       {/* Ideally check if user is admin. For now, show buttons if Pending and let backend reject if unauthorized */}
                       {leave.status === 'Pending' && (
                           <>
                               <button onClick={() => handleAction(leave.id, 'approve')} className="text-green-600 hover:text-green-800 font-medium text-xs">Approve</button>
                               <button onClick={() => handleAction(leave.id, 'reject')} className="text-red-600 hover:text-red-800 font-medium text-xs">Reject</button>
                           </>
                       )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-xl shadow-lg w-full max-w-md">
            <h2 className="text-xl font-bold mb-4">Apply for Leave</h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">Start Date</label>
                    <input
                    required
                    type="date"
                    className="w-full p-2 border rounded-lg"
                    value={formData.start_date}
                    onChange={(e) => setFormData({ ...formData, start_date: e.target.value })}
                    />
                </div>
                <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">End Date</label>
                    <input
                    required
                    type="date"
                    className="w-full p-2 border rounded-lg"
                    value={formData.end_date}
                    onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
                    />
                </div>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Reason</label>
                <textarea
                  required
                  rows="3"
                  className="w-full p-2 border rounded-lg"
                  value={formData.reason}
                  onChange={(e) => setFormData({ ...formData, reason: e.target.value })}
                ></textarea>
              </div>
              <div className="flex justify-end gap-2 mt-6">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                >
                  Apply
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
