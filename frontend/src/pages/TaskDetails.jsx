import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { 
  ArrowLeft, CheckCircle2, Clock, Calendar, User, 
  Plus, Trash2, Send, CheckSquare, Square, Save 
} from 'lucide-react';

export default function TaskDetails() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const [task, setTask] = useState(null);
  const [loading, setLoading] = useState(true);
  const [newChecklistItem, setNewChecklistItem] = useState('');
  const [notes, setNotes] = useState('');
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    fetchTask();
  }, [id]);

  const fetchTask = async () => {
    try {
      const response = await api.get(`/tasks/${id}/`);
      setTask(response.data);
      setNotes(response.data.completion_notes || '');
    } catch (error) {
      console.error('Error fetching task:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleChecklist = async (index) => {
    const updatedChecklist = [...task.checklist];
    updatedChecklist[index].completed = !updatedChecklist[index].completed;
    try {
      await api.patch(`/tasks/${id}/update_checklist/`, { checklist: updatedChecklist });
      setTask({ ...task, checklist: updatedChecklist });
    } catch (error) {
      console.error('Error updating checklist:', error);
    }
  };

  const addChecklistItem = async (e) => {
    e.preventDefault();
    if (!newChecklistItem.trim()) return;
    const updatedChecklist = [...task.checklist, { text: newChecklistItem, completed: false }];
    try {
      await api.patch(`/tasks/${id}/update_checklist/`, { checklist: updatedChecklist });
      setTask({ ...task, checklist: updatedChecklist });
      setNewChecklistItem('');
    } catch (error) {
      console.error('Error adding checklist item:', error);
    }
  };

  const updateStatus = async (newStatus) => {
    try {
      await api.patch(`/tasks/${id}/update_status/`, { status: newStatus });
      setTask({ ...task, status: newStatus });
    } catch (error) {
      console.error('Error updating status:', error);
    }
  };

  const saveNotes = async () => {
    setSaving(true);
    try {
      await api.patch(`/tasks/${id}/`, { completion_notes: notes });
      setTask({ ...task, completion_notes: notes });
      alert('Progress saved!');
    } catch (error) {
      console.error('Error saving progress:', error);
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="flex justify-center items-center h-full">Loading...</div>;
  if (!task) return <div>Task not found</div>;

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <button 
        onClick={() => navigate(-1)}
        className="flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
      >
        <ArrowLeft className="w-4 h-4" />
        Back to Tasks
      </button>

      <div className="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
        <div className="p-6 md:p-8 space-y-6">
          <div className="flex justify-between items-start">
            <div className="space-y-1">
              <span className={`px-2 py-1 rounded text-xs font-bold uppercase ${
                task.priority === 'high' ? 'text-red-600 bg-red-50' :
                task.priority === 'medium' ? 'text-amber-600 bg-amber-50' :
                'text-blue-600 bg-blue-50'
              }`}>
                {task.priority} Priority
              </span>
              <h1 className="text-3xl font-bold text-gray-900">{task.title}</h1>
              <p className="text-gray-500 font-medium">Project: {task.project_title}</p>
            </div>
            <select 
              className={`px-4 py-2 rounded-lg font-bold border-none ring-1 ring-gray-200 focus:ring-2 ${
                task.status === 'completed' ? 'bg-green-50 text-green-700' :
                task.status === 'in_progress' ? 'bg-blue-50 text-blue-700' :
                task.status === 'overdue' ? 'bg-red-50 text-red-700' :
                'bg-amber-50 text-amber-700'
              }`}
              value={task.status}
              onChange={(e) => updateStatus(e.target.value)}
            >
              <option value="pending">PENDING</option>
              <option value="in_progress">IN PROGRESS</option>
              <option value="completed">COMPLETED</option>
              <option value="overdue">OVERDUE</option>
            </select>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 py-6 border-y border-gray-50">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-indigo-50 rounded-lg text-indigo-600">
                <Calendar className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs text-gray-500 uppercase font-bold tracking-wider">Deadline</p>
                <p className="font-medium">{new Date(task.deadline).toLocaleDateString()}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="p-2 bg-amber-50 rounded-lg text-amber-600">
                <User className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs text-gray-500 uppercase font-bold tracking-wider">Assigned To</p>
                <p className="font-medium">{task.assigned_to_name}</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="p-2 bg-blue-50 rounded-lg text-blue-600">
                <Clock className="w-5 h-5" />
              </div>
              <div>
                <p className="text-xs text-gray-500 uppercase font-bold tracking-wider">Assigned By</p>
                <p className="font-medium">{task.assigned_by_name}</p>
              </div>
            </div>
          </div>

          <div className="space-y-3">
            <h3 className="text-lg font-bold text-gray-800">Description</h3>
            <p className="text-gray-600 leading-relaxed bg-gray-50 p-4 rounded-xl">
              {task.description}
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-lg font-bold text-gray-800">Checklist</h3>
                <span className="text-sm text-gray-500">
                  {task.checklist.filter(i => i.completed).length} / {task.checklist.length} done
                </span>
              </div>
              <div className="space-y-2">
                {task.checklist.map((item, idx) => (
                  <div key={idx} className="flex items-center gap-3 p-3 bg-white border border-gray-100 rounded-xl hover:border-indigo-100 transition-colors">
                    <button onClick={() => toggleChecklist(idx)}>
                      {item.completed ? (
                        <CheckSquare className="w-5 h-5 text-indigo-600" />
                      ) : (
                        <Square className="w-5 h-5 text-gray-300" />
                      )}
                    </button>
                    <span className={`flex-1 text-sm ${item.completed ? 'line-through text-gray-400' : 'text-gray-700'}`}>
                      {item.text}
                    </span>
                  </div>
                ))}
                <form onSubmit={addChecklistItem} className="flex gap-2 mt-4">
                  <input
                    type="text"
                    placeholder="Add subtask..."
                    className="flex-1 bg-gray-50 border border-gray-200 rounded-lg px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    value={newChecklistItem}
                    onChange={(e) => setNewChecklistItem(e.target.value)}
                  />
                  <button type="submit" className="p-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
                    <Plus className="w-5 h-5" />
                  </button>
                </form>
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="text-lg font-bold text-gray-800">Completion Notes</h3>
              <textarea
                placeholder="Add notes about your progress or work done..."
                className="w-full h-40 bg-gray-50 border border-gray-200 rounded-xl p-4 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                value={notes}
                onChange={(e) => setNotes(e.target.value)}
              />
              <button 
                onClick={saveNotes}
                disabled={saving}
                className="w-full flex items-center justify-center gap-2 bg-gray-900 text-white py-3 rounded-xl hover:bg-black transition-colors font-bold"
              >
                <Save className="w-5 h-5" />
                {saving ? 'Saving...' : 'Save Progress'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
