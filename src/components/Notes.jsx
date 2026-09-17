import { useEffect, useState } from 'react';
import { productivityAPI } from '../services/api';
import Loading from './Loading';
import ErrorMessage from './ErrorMessage';

export default function Notes() {
  const [notes, setNotes] = useState([]);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await productivityAPI.getNotes();
      setNotes((res && res.data) || []);
    } catch (err) {
      setError(err.message || 'Could not load notes.');
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
      await productivityAPI.createNote({ content: text.trim() });
      setText('');
      await load();
    } catch (err) {
      setError(err.message || 'Could not save the note.');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (noteId) => {
    setError('');
    try {
      await productivityAPI.deleteNote(noteId);
      setNotes((prev) => prev.filter((n) => n.id !== noteId));
    } catch (err) {
      setError(err.message || 'Could not delete the note.');
    }
  };

  return (
    <section className="panel panel--notes">
      <h2>Notes</h2>
      <p className="panel-subtitle">Quick thoughts and reminders</p>

      <form className="field-row" onSubmit={handleAdd}>
        <input
          type="text"
          placeholder="Write a note…"
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
        <Loading label="Loading notes…" />
      ) : notes.length === 0 ? (
        <p className="state-line">No notes yet.</p>
      ) : (
        <ul className="item-list">
          {notes.map((note) => (
            <li key={note.id} className="item-row">
              <div className="item-row-main">
                <span>{note.content}</span>
              </div>
              <button className="icon-btn" onClick={() => handleDelete(note.id)} aria-label="Delete note">
                ✕
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
