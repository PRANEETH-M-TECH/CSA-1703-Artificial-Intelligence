import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { AlertIcon, ChevronRightIcon } from "./Icons";

const TYPE_STYLE = {
  overlap: { label: "Overlap", cls: "border-coral-500/40 text-coral-400 bg-coral-500/10" },
  overdue: { label: "Overdue", cls: "border-amber-500/40 text-amber-400 bg-amber-500/10" },
  deadline_overrun: { label: "Deadline risk", cls: "border-accent-500/40 text-accent-400 bg-accent-500/10" },
};

export default function ConflictBanner({ conflict, trace, onExpand, onResolve }) {
  const [open, setOpen] = useState(false);
  const style = TYPE_STYLE[conflict.conflict_type] || TYPE_STYLE.overlap;

  const toggle = () => {
    setOpen((o) => !o);
    if (!open) onExpand?.(conflict);
  };

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: -12 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, x: 100, height: 0, marginBottom: 0 }}
      transition={{ duration: 0.3 }}
      className={`glass rounded-xl2 border overflow-hidden ${style.cls}`}
    >
      <button onClick={toggle} className="w-full flex items-center gap-3 p-4 text-left">
        <AlertIcon className="w-5 h-5 shrink-0" />
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-bold uppercase tracking-wide px-2 py-0.5 rounded-full bg-white/10">{style.label}</span>
          </div>
          <p className="text-sm text-slate-200 mt-1">{conflict.description}</p>
        </div>
        <motion.div animate={{ rotate: open ? 90 : 0 }}>
          <ChevronRightIcon className="w-5 h-5 text-slate-400" />
        </motion.div>
      </button>
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="px-4 pb-4"
          >
            <div className="bg-black/30 rounded-lg p-3 font-mono text-[11px] text-slate-400 space-y-1 mb-3">
              {(trace || ["Loading explanation trace..."]).map((line, i) => (
                <p key={i}>{line}</p>
              ))}
            </div>
            <p className="text-sm mb-3"><span className="text-slate-400">Suggested fix: </span>{conflict.suggestion}</p>
            <button
              onClick={() => onResolve?.(conflict)}
              className="w-full py-2.5 rounded-lg bg-grad-primary font-semibold text-sm hover:opacity-90 transition-opacity"
            >
              Open resolution
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
