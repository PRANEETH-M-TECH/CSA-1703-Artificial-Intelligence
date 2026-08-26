import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { motion } from "framer-motion";
import Sheet from "../components/Sheet";
import { ConflictsAPI } from "../api/client";

const OPTIONS = [
  { key: "reschedule", label: "Reschedule", desc: "Unschedule this task and let Module 1 re-place it on the next generation." },
  { key: "shorten", label: "Shorten duration", desc: "Cut the task's planned duration by ~40% so it can fit before its deadline." },
  { key: "drop", label: "Drop from schedule", desc: "Remove this task's slot entirely; it stays in your task list as pending." },
];

export default function ConflictResolution() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [conflict, setConflict] = useState(null);
  const [selected, setSelected] = useState("reschedule");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    ConflictsAPI.list().then((list) => setConflict(list.find((c) => String(c.id) === id)));
  }, [id]);

  const apply = async () => {
    setBusy(true);
    try {
      await ConflictsAPI.resolve(id, selected);
      navigate("/app/schedule/conflicts");
    } finally {
      setBusy(false);
    }
  };

  return (
    <Sheet title="Resolve conflict" onCloseTo="/app/schedule/conflicts">
      {conflict && (
        <p className="text-sm text-slate-400 mb-5 glass rounded-lg p-3">{conflict.description}</p>
      )}
      <div className="space-y-2 mb-6">
        {OPTIONS.map((opt) => (
          <label key={opt.key} className={`block p-4 rounded-xl2 cursor-pointer border transition-colors ${
            selected === opt.key ? "border-accent-500 bg-accent-500/10" : "border-white/10 bg-white/5"
          }`}>
            <div className="flex items-start gap-3">
              <div className="relative mt-0.5 shrink-0">
                <input type="radio" name="resolution" checked={selected === opt.key} onChange={() => setSelected(opt.key)} className="sr-only" />
                <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${selected === opt.key ? "border-accent-400" : "border-slate-500"}`}>
                  {selected === opt.key && (
                    <motion.div layoutId="radio-dot" className="w-2.5 h-2.5 rounded-full bg-accent-400" />
                  )}
                </div>
              </div>
              <div>
                <p className="font-semibold text-sm">{opt.label}</p>
                <p className="text-xs text-slate-400 mt-0.5">{opt.desc}</p>
              </div>
            </div>
          </label>
        ))}
      </div>
      <button onClick={apply} disabled={busy} className="w-full py-3.5 rounded-lg bg-grad-primary font-display font-bold shadow-glow disabled:opacity-50">
        {busy ? "Applying..." : "Apply resolution"}
      </button>
    </Sheet>
  );
}
