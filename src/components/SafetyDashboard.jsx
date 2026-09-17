import SafetyPlanner from './SafetyPlanner';
import DocumentVault from './DocumentVault';
import EmergencySupport from './EmergencySupport';
import QuickExit from './QuickExit';

export default function SafetyDashboard({ onExit }) {
  return (
    <div className="safety-page">
      <header className="safety-header">
        <h1>Safety Dashboard</h1>
        <QuickExit onExit={onExit} />
      </header>

      <div className="safety-body">
        <SafetyPlanner />
        <DocumentVault />
        <div style={{ gridColumn: '1 / -1' }}>
          <EmergencySupport />
        </div>
      </div>
    </div>
  );
}
