import { useState, useEffect } from 'react';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { Plus, Briefcase, Calendar, Clock, User, Trash2, Edit } from 'lucide-react';

export default function Projects() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [employees, setEmployees] = useState([]);
  const { user } = useAuth();
  const isAdmin = user?.role === 'admin';

  const [formData, setFormData] = useState({
    title: '',
    description: '',
    deadline: '',
    members: [''], // Initialize with one empty member slot
    status: 'pending'
  });

  const addMemberField = () => {
    setFormData({ ...formData, members: [...formData.members, ''] });
  };

  const updateMember = (index, value) => {
    const newMembers = [...formData.members];
    newMembers[index] = value;
    setFormData({ ...formData, members: newMembers });
  };

  const removeMemberField = (index) => {
    const newMembers = formData.members.filter((_, i) => i !== index);
    setFormData({ ...formData, members: newMembers });
  };

  useEffect(() => {
    fetchProjects();
    if (isAdmin) fetchEmployees();
  }, [isAdmin]);

  const fetchProjects = async () => {
    try {
      const response = await api.get('projects/');
      setProjects(response.data);
    } catch (error) {
      console.error('Error fetching projects:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchEmployees = async () => {
    try {
      const response = await api.get('employees/');
      setEmployees(response.data);
    } catch (error) {
      console.error('Error fetching employees:', error);
    }
  };

  const handleEdit = (project) => {
    setIsEditing(true);
    setEditingId(project.id);
    setFormData({
      title: project.title,
      description: project.description,
      deadline: project.deadline,
      members: project.members && project.members.length > 0 ? project.members : [''],
      status: project.status
    });
    setShowModal(true);
  };

  const openCreateModal = () => {
    setIsEditing(false);
    setEditingId(null);
    setFormData({ title: '', description: '', deadline: '', members: [''], status: 'pending' });
    setShowModal(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Filter out empty member slots
      const cleanMembers = formData.members.filter(m => m !== '');
      if (cleanMembers.length === 0) {
        alert("Please assign at least one member.");
        return;
      }

      const payload = {
        ...formData,
        members: cleanMembers
      };

      if (isEditing) {
        await api.put(`projects/${editingId}/`, payload);
        alert("Project updated successfully!");
      } else {
        await api.post('projects/', payload);
        alert("Project created successfully!");
      }
      
      setShowModal(false);
      setFormData({ title: '', description: '', deadline: '', members: [''], status: 'pending' });
      fetchProjects();
    } catch (error) {
      console.error('Error saving project:', error);
      const errorMsg = error.response?.data 
        ? Object.entries(error.response.data).map(([k, v]) => `${k}: ${v}`).join('\n')
        : error.message;
      alert("Failed to save project:\n" + errorMsg);
    }
  };

  const deleteProject = async (id) => {
    if (window.confirm('Are you sure you want to delete this project?')) {
      try {
        await api.delete(`projects/${id}/`);
        fetchProjects();
      } catch (error) {
        console.error('Error deleting project:', error);
      }
    }
  };

  if (loading) return <div className="flex justify-center items-center h-full">Loading...</div>;

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Projects</h1>
          <p className="text-gray-500">Manage and track company projects</p>
        </div>
        {isAdmin && (
          <button
            onClick={openCreateModal}
            className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors shadow-sm"
          >
            <Plus className="w-5 h-5" />
            New Project
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {projects.map((project) => (
          <div key={project.id} className="bg-white rounded-xl border border-gray-100 shadow-sm hover:shadow-md transition-all duration-300 p-5 space-y-4">
            <div className="flex justify-between items-start">
              <div className="p-2 bg-blue-50 rounded-lg">
                <Briefcase className="w-6 h-6 text-blue-600" />
              </div>
              <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                project.status === 'completed' ? 'bg-green-100 text-green-700' :
                project.status === 'in_progress' ? 'bg-blue-100 text-blue-700' :
                'bg-amber-100 text-amber-700'
              }`}>
                {project.status.replace('_', ' ').toUpperCase()}
              </span>
            </div>
            
            <div>
              <h3 className="text-lg font-bold text-gray-800">{project.title}</h3>
              <p className="text-gray-500 text-sm line-clamp-2 mt-1">{project.description}</p>
            </div>

            <div className="grid grid-cols-2 gap-4 pt-2">
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <Calendar className="w-4 h-4" />
                <span>{new Date(project.deadline).toLocaleDateString()}</span>
              </div>
              <div className="flex items-center gap-2 text-sm text-gray-600">
                <User className="w-4 h-4" />
                <span>{project.members.length} Members</span>
              </div>
            </div>

            {isAdmin && (
              <div className="flex justify-end gap-2 pt-4 border-t border-gray-50">
                <button 
                    onClick={() => handleEdit(project)}
                    className="p-2 text-gray-400 hover:text-blue-600 transition-colors"
                >
                  <Edit className="w-4 h-4" />
                </button>
                <button 
                  onClick={() => deleteProject(project.id)}
                  className="p-2 text-gray-400 hover:text-red-600 transition-colors"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            )}
          </div>
        ))}
      </div>

      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex justify-center items-center z-50 p-4 backdrop-blur-sm">
          <div className="bg-white rounded-2xl w-full max-w-lg p-6 space-y-4 shadow-2xl overflow-y-auto max-h-[90vh]">
            <h2 className="text-xl font-bold text-gray-900 border-b pb-2">
                {isEditing ? 'Edit Project' : 'Create New Project'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Project Title</label>
                <input
                  required
                  type="text"
                  placeholder="Enter project name"
                  className="mt-1 block w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500 outline-none"
                  value={formData.title}
                  onChange={(e) => setFormData({...formData, title: e.target.value})}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Description</label>
                <textarea
                  required
                  placeholder="What is this project about?"
                  className="mt-1 block w-full border border-gray-300 rounded-lg p-2.5 h-24 focus:ring-2 focus:ring-blue-500 outline-none"
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Deadline</label>
                  <input
                    required
                    type="date"
                    className="mt-1 block w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500 outline-none"
                    value={formData.deadline}
                    onChange={(e) => setFormData({...formData, deadline: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
                  <select
                    className="mt-1 block w-full border border-gray-300 rounded-lg p-2.5 focus:ring-2 focus:ring-blue-500 outline-none bg-white"
                    value={formData.status}
                    onChange={(e) => setFormData({...formData, status: e.target.value})}
                  >
                    <option value="pending">Pending</option>
                    <option value="in_progress">In Progress</option>
                    <option value="completed">Completed</option>
                  </select>
                </div>
              </div>
              
              <div className="space-y-2">
                <div className="flex justify-between items-center">
                    <label className="block text-sm font-medium text-gray-700">Assign Members</label>
                    <button 
                        type="button"
                        onClick={addMemberField}
                        className="text-xs bg-blue-50 text-blue-600 px-2 py-1 rounded-md hover:bg-blue-100 font-bold flex items-center gap-1"
                    >
                        <Plus className="w-3 h-3" /> Add Member
                    </button>
                </div>
                
                <div className="space-y-2 max-h-48 overflow-y-auto p-1">
                    {formData.members.map((memberId, index) => (
                        <div key={index} className="flex gap-2">
                            <select
                                required
                                className="flex-1 border border-gray-300 rounded-lg p-2 bg-white outline-none focus:ring-2 focus:ring-blue-500"
                                value={memberId}
                                onChange={(e) => updateMember(index, e.target.value)}
                            >
                                <option value="">Select Member</option>
                                {employees.map(emp => (
                                    <option key={emp.id} value={emp.id}>{emp.name} ({emp.employee_id})</option>
                                ))}
                            </select>
                            {formData.members.length > 1 && (
                                <button 
                                    type="button"
                                    onClick={() => removeMemberField(index)}
                                    className="text-red-500 hover:bg-red-50 p-2 rounded-lg"
                                >
                                    <Trash2 className="w-4 h-4" />
                                </button>
                            )}
                        </div>
                    ))}
                </div>
              </div>

              <div className="flex justify-end gap-3 pt-4 border-t">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg font-medium"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-bold shadow-md transition-all active:scale-95"
                >
                  {isEditing ? 'Update Project' : 'Create Project'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
