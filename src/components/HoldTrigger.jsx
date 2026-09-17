import useHoldTrigger from '../hooks/useHoldTrigger';

/**
 * Wraps any element in a press-and-hold interaction. Renders no extra DOM
 * (just clones-in behaviour via a plain span) and exposes only a subtle
 * CSS variable (--hold-pct) so the parent can render a faint progress cue
 * without any explanatory text.
 */
export default function HoldTrigger({ duration = 2500, onHoldComplete, children, className }) {
  const { bind, progress } = useHoldTrigger({ duration, onHoldComplete });

  return (
    <span
      {...bind}
      className={className}
      style={{ ...bind.style, '--hold-pct': `${Math.round(progress * 100)}%` }}
    >
      {children}
    </span>
  );
}
