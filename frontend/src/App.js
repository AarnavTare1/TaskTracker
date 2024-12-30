import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState('');
  const [editingTaskId, setEditingTaskId] = useState(null);
  const [editingTitle, setEditingTitle] = useState('');

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:5000/api/tasks/');
      setTasks(res.data);
    } catch (error) {
      console.error(error);
    }
  };

  const handleCreateTask = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    try {
      const res = await axios.post('http://127.0.0.1:5000/api/tasks/', {
        title,
        completed: false,
      });
      setTasks([...tasks, res.data]);
      setTitle('');
    } catch (error) {
      console.error(error);
    }
  };

  // Toggle "completed"
  const handleToggleComplete = async (taskId, currentStatus) => {
    try {
      const res = await axios.put(`http://127.0.0.1:5000/api/tasks/${taskId}`, {
        completed: !currentStatus,
      });
      const updated = res.data;
      setTasks((prev) => prev.map((t) => (t.id === taskId ? updated : t)));
    } catch (error) {
      console.error(error);
    }
  };

  // Edit
  const handleEditClick = (task) => {
    setEditingTaskId(task.id);
    setEditingTitle(task.title);
  };

  const handleCancelEdit = () => {
    setEditingTaskId(null);
    setEditingTitle('');
  };

  const handleSaveEdit = async (taskId) => {
    try {
      const res = await axios.put(`http://127.0.0.1:5000/api/tasks/${taskId}`, {
        title: editingTitle,
      });
      const updatedTask = res.data;
      setTasks((prev) => prev.map((t) => (t.id === taskId ? updatedTask : t)));
      setEditingTaskId(null);
      setEditingTitle('');
    } catch (error) {
      console.error(error);
    }
  };

  const handleDeleteTask = async (taskId) => {
    try {
      await axios.delete(`http://127.0.0.1:5000/api/tasks/${taskId}`);
      setTasks((prev) => prev.filter((t) => t.id !== taskId));
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div style={{ margin: '40px' }}>
      <h1>Task Tracker</h1>

      <form onSubmit={handleCreateTask} style={{ marginBottom: '20px' }}>
        <input
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="New Task"
        />
        <button type="submit">Add Task</button>
      </form>

      {tasks.length === 0 ? (
        <p>No tasks yet.</p>
      ) : (
        <ul style={{ listStyle: 'none', paddingLeft: 0 }}>
          {tasks.map((task) => {
            const isEditing = task.id === editingTaskId;
            return (
              <li key={task.id} style={{ marginBottom: '8px' }}>
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => handleToggleComplete(task.id, task.completed)}
                />
                {isEditing ? (
                  <>
                    <input
                      type="text"
                      value={editingTitle}
                      onChange={(e) => setEditingTitle(e.target.value)}
                      style={{ marginLeft: '10px' }}
                    />
                    <button onClick={() => handleSaveEdit(task.id)}>Save</button>
                    <button onClick={handleCancelEdit}>Cancel</button>
                  </>
                ) : (
                  <>
                    <span
                      style={{
                        textDecoration: task.completed ? 'line-through' : 'none',
                        marginLeft: '10px',
                      }}
                    >
                      {task.title}
                    </span>
                    <button onClick={() => handleEditClick(task)}>Edit</button>
                  </>
                )}
                <button onClick={() => handleDeleteTask(task.id)} style={{ marginLeft: '10px' }}>
                  Delete
                </button>
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
}

export default App;
