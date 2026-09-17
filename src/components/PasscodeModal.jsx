import { useState } from 'react';
import ErrorMessage from './ErrorMessage';
import { authAPI } from '../services/api';

/**
 * Deliberately generic copy: no "Safety", "secret", or "unlock" wording
 * visible in the UI text, in case someone is looking over the user's
 * shoulder while this is open.
 */
export default function PasscodeModal({ onSuccess, onClose }) {
  const [passcode, setPasscode] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!passcode.trim()) {
      setError('Enter a code to continue.');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const res = await authAPI.unlock(passcode.trim());
      if (res && res.success) {
        onSuccess();
      } else {
        setError((res && res.message) || 'That code is not recognized.');
      }
    } catch (err) {
      setError(err.message || 'Something went wrong. Try again.');
    } finally {
      setLoading(false);
      setPasscode('');
    }
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <form onSubmit={handleSubmit}>
          <h3>Verification code</h3>
          <p className="hint">Enter your code to continue.</p>
          <input
            type="password"
            inputMode="text"
            autoFocus
            value={passcode}
            onChange={(e) => setPasscode(e.target.value)}
            placeholder="••••••"
            disabled={loading}
          />
          <ErrorMessage message={error} />
          <div className="modal-actions">
            <button type="button" className="btn btn-ghost" onClick={onClose} disabled={loading}>
              Cancel
            </button>
            <button type="submit" className="btn" disabled={loading}>
              {loading ? 'Checking…' : 'Continue'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
