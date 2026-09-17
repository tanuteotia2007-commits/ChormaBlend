import { useEffect, useState } from 'react';
import ProductivityPage from './pages/ProductivityPage';
import SafetyPage from './pages/SafetyPage';
import { authAPI } from './services/api';

export default function App() {
  const [view, setView] = useState('productivity'); // 'productivity' | 'safety'
  const [checkingSession, setCheckingSession] = useState(false);

  // The passcode modal already confirms unlock via POST /auth/unlock. Right
  // after that, we re-confirm with the backend session-status endpoint so
  // the dashboard is never shown on frontend state alone (rule: backend is
  // the authority on authorization).
  const handleUnlocked = async () => {
    setCheckingSession(true);
    try {
      const res = await authAPI.status();
      if (res && res.authenticated) {
        setView('safety');
      }
      // If the backend disagrees, silently stay on the productivity page —
      // no error dialog, to avoid drawing attention to the failed attempt.
    } catch {
      // Network/backend failure: stay on the visible page.
    } finally {
      setCheckingSession(false);
    }
  };

  const handleExit = () => {
    setView('productivity');
  };

  // If a safety-area API call ever comes back 401/403, components bubble
  // that up as a normal error message. As a hard backstop, re-check session
  // status whenever the safety view is active and something invalidates it.
  useEffect(() => {
    if (view !== 'safety') return;
    let cancelled = false;
    authAPI
      .status()
      .then((res) => {
        if (!cancelled && (!res || !res.authenticated)) {
          setView('productivity');
        }
      })
      .catch(() => {
        // If the status check itself fails, don't force an exit — a flaky
        // network call shouldn't kick someone out mid-task.
      });
    return () => {
      cancelled = true;
    };
  }, [view]);

  if (view === 'safety') {
    return <SafetyPage onExit={handleExit} />;
  }

  return <ProductivityPage onUnlocked={handleUnlocked} />;
}
