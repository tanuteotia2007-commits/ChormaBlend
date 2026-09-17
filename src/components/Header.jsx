import { useState } from 'react';
import HoldTrigger from './HoldTrigger';
import PasscodeModal from './PasscodeModal';

export default function Header({ onUnlocked }) {
  const [showPasscode, setShowPasscode] = useState(false);

  return (
    <header className="workspace-header">
      <HoldTrigger
        duration={2500}
        onHoldComplete={() => setShowPasscode(true)}
        className="workspace-wordmark"
      >
        <span className="workspace-hold-ring" aria-hidden="true" />
        <span className="swatch-cluster" aria-hidden="true">
          <span className="swatch" style={{ background: 'var(--ws-indigo)' }} />
          <span className="swatch" style={{ background: 'var(--ws-teal)' }} />
          <span className="swatch" style={{ background: 'var(--ws-amber)' }} />
        </span>
        Chroma Blend
      </HoldTrigger>

      <nav className="workspace-nav">Notes · To-Do · Planner</nav>

      {showPasscode && (
        <PasscodeModal
          onClose={() => setShowPasscode(false)}
          onSuccess={() => {
            setShowPasscode(false);
            onUnlocked();
          }}
        />
      )}
    </header>
  );
}
