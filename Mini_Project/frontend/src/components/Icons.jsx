// Lightweight inline SVG icon set — no external icon dependency.
const base = { fill: "none", stroke: "currentColor", strokeWidth: 2, strokeLinecap: "round", strokeLinejoin: "round" };

export const HomeIcon = (p) => (
  <svg viewBox="0 0 24 24" {...base} {...p}><path d="M3 11.5 12 4l9 7.5" /><path d="M5 10v10h14V10" /></svg>
);
export const ListIcon = (p) => (
  <svg viewBox="0 0 24 24" {...base} {...p}><path d="M8 6h13M8 12h13M8 18h13" /><circle cx="3.5" cy="6" r="1.5" fill="currentColor" stroke="none" /><circle cx="3.5" cy="12" r="1.5" fill="currentColor" stroke="none" /><circle cx="3.5" cy="18" r="1.5" fill="currentColor" stroke="none" /></svg>
);
export const CalendarIcon = (p) => (
  <svg viewBox="0 0 24 24" {...base} {...p}><rect x="3" y="5" width="18" height="16" rx="2" /><path d="M3 10h18M8 3v4M16 3v4" /></svg>
);
export const ChartIcon = (p) => (
  <svg viewBox="0 0 24 24" {...base} {...p}><path d="M4 20V10M12 20V4M20 20v-7" /></svg>
);
export const UserIcon = (p) => (
  <svg viewBox="0 0 24 24" {...base} {...p}><circle cx="12" cy="8" r="4" /><path d="M4 20c1.5-4 5-6 8-6s6.5 2 8 6" /></svg>
);
export const PlusIcon = (p) => (
  <svg viewBox="0 0 24 24" {...base} {...p}><path d="M12 5v14M5 12h14" /></svg>
);
export const CloseIcon = (p) => (
  <svg viewBox="0 0 24 24" {...base} {...p}><path d="M6 6l12 12M18 6 6 18" /></svg>
);
export const CheckIcon = (p) => (
  <svg viewBox="0 0 24 24" {...base} {...p}><path d="M20 6 9 17l-5-5" /></svg>
);
export const AlertIcon = (p) => (
  <svg viewBox="0 0 24 24" {...base} {...p}><path d="M12 9v4M12 17h.01" /><path d="M10.3 3.9 1.9 18a2 2 0 0 0 1.7 3h16.8a2 2 0 0 0 1.7-3L14.1 3.9a2 2 0 0 0-3.8 0Z" /></svg>
);
export const ChevronRightIcon = (p) => (
  <svg viewBox="0 0 24 24" {...base} {...p}><path d="m9 6 6 6-6 6" /></svg>
);
export const TrashIcon = (p) => (
  <svg viewBox="0 0 24 24" {...base} {...p}><path d="M3 6h18M8 6V4h8v2M6 6l1 14h10l1-14" /></svg>
);
export const SparkleIcon = (p) => (
  <svg viewBox="0 0 24 24" {...base} {...p}><path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2 2M16 16l2 2M6 18l2-2M16 8l2-2" /></svg>
);
export const LogoutIcon = (p) => (
  <svg viewBox="0 0 24 24" {...base} {...p}><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" /><path d="M16 17l5-5-5-5" /><path d="M21 12H9" /></svg>
);

export function LogoMark({ className = "w-8 h-8" }) {
  return (
    <div className={`${className} rounded-lg bg-grad-primary flex items-center justify-center shadow-glow`}>
      <svg viewBox="0 0 24 24" width="60%" height="60%" fill="none" stroke="white" strokeWidth={2.5} strokeLinecap="round" strokeLinejoin="round">
        <path d="M5 12.5 10 17.5 19 6.5" />
      </svg>
    </div>
  );
}
