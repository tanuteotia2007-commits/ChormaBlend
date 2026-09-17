import { useEffect, useState } from 'react';
import { productivityAPI } from '../services/api';
import Loading from './Loading';
import ErrorMessage from './ErrorMessage';

export default function Planner() {
  const [items, setItems] = useState([]);
  const [title, setTitle] = useState('');
  const [when, setWhen] = useState('');
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState('');

  const load = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await productivityAPI.getPlanner();
      setItems((res && res.data) || []);
    } catch (err) {
      setError(err.message || 'Could not load the planner.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const handleAdd = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    setSaving(true);
    setError('');
    try {
      await productivityAPI.createPlannerItem({ title: title.trim(), scheduled_for: when || null });
      setTitle('');
      setWhen('');
      await load();
    } catch (err) {
      setError(err.message || 'Could not save the plan item.');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (itemId) => {
    setError('');
    try {
      await productivityAPI.deletePlannerItem(itemId);
      setItems((prev) => prev.filter((i) => i.id !== itemId));
    } catch (err) {
      setError(err.message || 'Could not delete the plan item.');
    }
  };

  return (
    <section className="panel panel--planner">
      <h2>Planner</h2>
      <p className="panel-subtitle">Upcoming plans</p>

      <form onSubmit={handleAdd}>
        <div className="field-row">
          <input
            type="text"
            placeholder="What's the plan?"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            disabled={saving}
          />
        </div>
        <div className="field-row">
          <input
            type="date"
            value={when}
            onChange={(e) => setWhen(e.target.value)}
            disabled={saving}
          />
          <button className="btn" type="submit" disabled={saving || !title.trim()}>
            {saving ? 'Adding…' : 'Add'}
          </button>
        </div>
      </form>

      <ErrorMessage message={error} />

      {loading ? (
        <Loading label="Loading planner…" />
      ) : items.length === 0 ? (
        <p className="state-line">Nothing planned yet.</p>
      ) : (
        <ul className="item-list">
          {items.map((item) => (
            <li key={item.id} className="item-row">
              <div className="item-row-main">
                <span>
                  {item.title}
                  {item.scheduled_for ? ` — ${item.scheduled_for}` : ''}
                </span>
              </div>
              <button className="icon-btn" onClick={() => handleDelete(item.id)} aria-label="Delete plan item">
                ✕
              </button>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
