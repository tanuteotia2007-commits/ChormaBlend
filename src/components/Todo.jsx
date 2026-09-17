import { useEffect, useState } from 'react';
import { productivityAPI } from '../services/api';
import Loading from './Loading';
import ErrorMessage from './ErrorMessage';

export default function Todo() {
  const [todos, setTodos] = useState([]);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await productivityAPI.getTodos();
      setTodos((res && res.data) || []);
    } catch (err) {
      setError(err.message || 'Could not load tasks.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleAdd = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    setSaving(true);
    setError('');
    try {
      await productivityAPI.createTodo({ task: text.trim(), completed: false });
      setText('');
      await load();
    } catch (err) {
      setError(err.message || 'Could not save the task.');
    } finally {
      setSaving(false);
    }
  };

  const handleToggle = async (todo) => {
    setError('');
    // optimistic update, reconciled against backend response
    setTodos((prev) =>
      prev.map((t) => (t.id === todo.id ? { ...t, completed: !t.completed } : t))
    );
    try {
      await productivityAPI.updateTodo(todo.id, { completed: !todo.completed });
    } catch (err) {
      setError(err.message || 'Could not update the task.');
      await load(); // roll back to backend truth
    }
  };

  const handleDelete = async (todoId) => {
    setError('');
    try {
      await productivityAPI.deleteTodo(todoId);
      setTodos((prev) => prev.filter((t) => t.id !== todoId));
    } catch (err) {
      setError(err.message || 'Could not delete the task.');
    }
  };

  return (
    <section className="panel panel--todo">
      <h2>To-Do</h2>
      <p className="panel-subtitle">Today's tasks</p>

      <form className="field-row" onSubmit={handleAdd}>
        <input
          type="text"
          placeholder="Add a task…"
          value={text}
          onChange={(e) => setText(e.target.value)}
          disabled={saving}
        />
        <button className="btn" type="submit" disabled={saving || !text.trim()}>
          {saving ? 'Adding…' : 'Add'}
        </button>
      </form>

      <ErrorMessage message={error} />

      {loading ? (
        <Loading label="Loading tasks…" />
      ) : todos.length === 0 ? (
        <p className="state-line">No tasks yet.</p>
      ) : (
        <ul className="item-list">
          {todos.map((todo) => (
            <li key={todo.id} className={`item-row ${todo.completed ? 'completed' : ''}`}>
              <div className="item-row-main">
                <input
                  type="checkbox"
                  checked={!!todo.completed}
                  onChange={() => handleToggle(todo)}
                />
                <span>{todo.task}</span>
              </div>
              <button className="icon-btn" onClick={() => handleDelete(todo.id)} aria-label="Delete task">
                ✕
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
