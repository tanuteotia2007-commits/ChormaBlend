import { useState } from 'react';
import { authAPI } from '../services/api';

export default function QuickExit({ onExit }) {
  const [exiting, setExiting] = useState(false);

  const handleExit = async () => {
    setExiting(true);
    // Clear frontend state immediately regardless of backend timing, so the
    // screen changes right away even on a slow connection.
    onExit();
    try {
      await authAPI.exit();
    } catch {
      // Even if the request fails, the user is already back on the
      // productivity workspace client-side. The next auth/status check
      // will re-confirm the real backend session state.
    } finally {
      setExiting(false);
    }
  };

  return (
    <button className="btn-quiet" onClick={handleExit} disabled={exiting}>
      {exiting ? 'Leaving…' : 'Quick exit'}
    </button>
  );
}
