import { useRef, useCallback, useState } from 'react';

/**
 * useHoldTrigger
 *
 * Fires `onHoldComplete` only after the pointer/touch has been held down
 * continuously for `duration` ms. A short tap/click never fires it.
 *
 * Usage:
 *   const { bind, progress } = useHoldTrigger({ duration: 2500, onHoldComplete });
 *   <h1 {...bind}>Chroma Blend</h1>
 *
 * `progress` (0–1) can optionally be used for a subtle visual cue, but the
 * component using this hook should NOT reveal what the interaction does.
 */
export default function useHoldTrigger({ duration = 2500, onHoldComplete }) {
  const timerRef = useRef(null);
  const startTimeRef = useRef(null);
  const firedRef = useRef(false);
  const [progress, setProgress] = useState(0);
  const [isHolding, setIsHolding] = useState(false);

  const clearTimer = useCallback(() => {
    if (timerRef.current) {
      cancelAnimationFrame(timerRef.current);
      timerRef.current = null;
    }
  }, []);

  const tick = useCallback(() => {
    if (!startTimeRef.current) return;
    const elapsed = Date.now() - startTimeRef.current;
    const pct = Math.min(elapsed / duration, 1);
    setProgress(pct);

    if (pct >= 1 && !firedRef.current) {
      firedRef.current = true;
      setIsHolding(false);
      clearTimer();
      onHoldComplete && onHoldComplete();
      return;
    }
    timerRef.current = requestAnimationFrame(tick);
  }, [duration, onHoldComplete, clearTimer]);

  const start = useCallback(
    (e) => {
      // Ignore secondary mouse buttons / already-in-progress holds
      if (e.type === 'mousedown' && e.button !== 0) return;
      firedRef.current = false;
      startTimeRef.current = Date.now();
      setIsHolding(true);
      setProgress(0);
      clearTimer();
      timerRef.current = requestAnimationFrame(tick);
    },
    [tick, clearTimer]
  );

  const cancel = useCallback(() => {
    startTimeRef.current = null;
    setIsHolding(false);
    setProgress(0);
    clearTimer();
  }, [clearTimer]);

  const bind = {
    onMouseDown: start,
    onMouseUp: cancel,
    onMouseLeave: cancel,
    onTouchStart: start,
    onTouchEnd: cancel,
    onTouchCancel: cancel,
    // Prevent the native context menu / text selection from interrupting
    // a long-press on touch devices.
    onContextMenu: (e) => e.preventDefault(),
    style: { userSelect: 'none', WebkitUserSelect: 'none', touchAction: 'manipulation' },
  };

  return { bind, progress, isHolding };
}
