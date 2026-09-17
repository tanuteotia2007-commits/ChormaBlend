export default function Loading({ label = 'Loading…' }) {
  return (
    <p className="state-line">
      <span className="spinner" aria-hidden="true" />
      {label}
    </p>
  );
}
