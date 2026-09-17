import { useState } from 'react';
import { aiAPI } from '../services/api';
import Loading from './Loading';
import ErrorMessage from './ErrorMessage';

export default function SafetyPlanner() {
  const [situation, setSituation] = useState('');
  const [urgency, setUrgency] = useState('low');
  const [locationContext, setLocationContext] = useState('');
  const [preferences, setPreferences] = useState('');
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!situation.trim()) {
      setError('Describe your situation so a plan can be generated.');
      return;
    }
    setLoading(true);
    setError('');
    setPlan(null);
    try {
      const res = await aiAPI.getSafetyPlan({
        situation: situation.trim(),
        urgency,
        location_context: locationContext.trim(),
        preferences: preferences.trim(),
      });
      if (res && res.success && Array.isArray(res.plan)) {
        setPlan(res.plan);
      } else {
        setError((res && res.message) || 'Could not generate a plan right now.');
      }
    } catch (err) {
      setError(err.message || 'The planning service is unavailable right now.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="safety-card">
      <h2>Safety Planner</h2>
      <p className="desc">Describe your situation to get calm, practical next steps.</p>

      <form onSubmit={handleSubmit}>
        <textarea
          className="safety-textarea"
          rows={3}
          placeholder="What's going on?"
          value={situation}
          onChange={(e) => setSituation(e.target.value)}
          disabled={loading}
        />
        <select
          className="safety-select"
          value={urgency}
          onChange={(e) => setUrgency(e.target.value)}
          disabled={loading}
        >
          <option value="low">Not urgent</option>
          <option value="medium">Somewhat urgent</option>
          <option value="high">Urgent</option>
        </select>
        <input
          className="safety-input"
          type="text"
          placeholder="Where are you right now? (optional)"
          value={locationContext}
          onChange={(e) => setLocationContext(e.target.value)}
          disabled={loading}
        />
        <input
          className="safety-input"
          type="text"
          placeholder="Anything specific you want the plan to consider? (optional)"
          value={preferences}
          onChange={(e) => setPreferences(e.target.value)}
          disabled={loading}
        />
        <button className="btn-accent" type="submit" disabled={loading || !situation.trim()}>
          {loading ? 'Generating…' : 'Get a plan'}
        </button>
      </form>

      <ErrorMessage message={error} />
      {loading && <Loading label="Generating your plan…" />}

      {plan && (
        <ol className="plan-steps" style={{ marginTop: 14 }}>
          {plan.map((step, i) => (
            <li key={i}>{step}</li>
          ))}
        </ol>
      )}
    </div>
  );
}
