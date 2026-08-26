import { useEffect, useState } from "react";
import { useNavigate, Outlet } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { ScheduleAPI, ConflictsAPI } from "../api/client";

const DAY_MS = 86400000;
const CAT_COLOR = {
  Study: "from-accent-500 to-accent-400", Work: "from-mint-500 to-mint-400",
  Fitness: "from-coral-500 to-coral-400", Personal: "from-amber-500 to-amber-400",
  Meeting: "from-accent-600 to-mint-500", General: "from-slate-500 to-slate-400",
};

function startOfDay(d) { const x = new Date(d); x.setHours(0, 0, 0, 0); return x; }

export default function ScheduleView() {
  const [entries, setEntries] = useState([]);
  const [conflicts, setConflicts] = useState([]);
  const [generating, setGenerating] = useState(false);
  const [loading, setLoading] = useState(true);
  const [dayOffset, setDayOffset] = useState(0);
  const [lastRun, setLastRun] = useState(null);
  const navigate = useNavigate();

  const load = () => Promise.all([ScheduleAPI.get(), ConflictsAPI.list()]).then(([s, c]) => { setEntries(s); setConflicts(c); }).finally(() => setLoading(false));
  useEffect(() => { load(); }, []);

  const generate = async () => {
    setGenerating(true);
    try {
      const res = await ScheduleAPI.generate();
      setLastRun(res);
      await ConflictsAPI.check();
      await load();
    } finally {
      setGenerating(false);
    }
  };

  const day = new Date(startOfDay(Date.now()).getTime() + dayOffset * DAY_MS);
  const dayEntries = entries.filter((e) => startOfDay(e.start_time).getTime() === day.getTime()).sort((a, b) => new Date(a.start_time) - new Date(b.start_time));
  const conflictedTaskIds = new Set(conflicts.flatMap((c) => [c.task_a_id, c.task_b_id]).filter(Boolean));

  const HOUR_START = 6, HOUR_END = 22;
  const hours = Array.from({ length: HOUR_END - HOUR_START }, (_, i) => HOUR_START + i);

  return (
    <div className="p-6 max-w-4xl mx-auto pb-16">
      <div className="flex items-center justify-between mb-4 flex-wrap gap-3">
        <h1 className="text-2xl font-display font-bold">Schedule</h1>
        <div className="flex items-center gap-3">
          {conflicts.length > 0 && (
            <button onClick={() => navigate("/app/schedule/conflicts")} className="px-3 py-2 rounded-lg bg-coral-500/15 text-coral-400 text-xs font-semibold">
              {conflicts.length} conflict{conflicts.length > 1 ? "s" : ""}
            </button>
          )}
          <button onClick={generate} disabled={generating}
            className="px-4 py-2.5 rounded-lg bg-grad-primary text-sm font-semibold shadow-glow disabled:opacity-60 flex items-center gap-2">
            {generating && <span className="w-4 h-4 rounded-full border-2 border-white/60 border-t-transparent animate-spin" />}
            {generating ? "Generating..." : "Generate schedule"}
          </button>
        </div>
      </div>

      {lastRun && (
        <motion.p initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="text-xs text-slate-500 mb-4">
          Module 1 ({lastRun.algorithm}) placed {lastRun.entries.length} task(s)
          {lastRun.unscheduled_task_ids.length > 0 && `, ${lastRun.unscheduled_task_ids.length} couldn't fit`}.
        </motion.p>
      )}

      <div className="flex items-center justify-between mb-3">
        <button onClick={() => setDayOffset((d) => d - 1)} className="px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-sm">‹</button>
        <p className="font-semibold text-sm">{day.toLocaleDateString(undefined, { weekday: "long", month: "short", day: "numeric" })}</p>
        <button onClick={() => setDayOffset((d) => d + 1)} className="px-3 py-1.5 rounded-lg bg-white/5 hover:bg-white/10 text-sm">›</button>
      </div>

      {loading ? (
        <div className="glass rounded-xl2 h-64 animate-pulse" />
      ) : (
        <div className="glass rounded-xl2 p-4 sm:hidden">
          {dayEntries.length === 0 ? (
            <p className="text-center text-slate-400 py-10 text-sm">Nothing scheduled this day.</p>
          ) : (
            <div className="space-y-2">
              {dayEntries.map((e) => (
                <AgendaCard key={e.id} entry={e} flagged={conflictedTaskIds.has(e.task_id)} onClick={() => navigate("/app/schedule/conflicts")} />
              ))}
            </div>
          )}
        </div>
      )}

      {/* Desktop/tablet grid */}
      {!loading && (
        <div className="hidden sm:block glass rounded-xl2 p-4 overflow-x-auto">
          <div className="relative min-w-[500px]" style={{ height: hours.length * 56 }}>
            {hours.map((h, i) => (
              <div key={h} className="absolute left-0 right-0 border-t border-white/5 flex items-start" style={{ top: i * 56 }}>
                <span className="text-[10px] text-slate-500 w-12 -mt-2">{h}:00</span>
              </div>
            ))}
            <div className="absolute left-14 right-0 top-0 bottom-0">
              <AnimatePresence>
                {dayEntries.map((e) => {
                  const start = new Date(e.start_time);
                  const end = new Date(e.end_time);
                  const top = Math.max(0, (start.getHours() + start.getMinutes() / 60 - HOUR_START) * 56);
                  const height = Math.max(28, ((end - start) / 3600000) * 56);
                  const flagged = conflictedTaskIds.has(e.task_id);
                  return (
                    <motion.button
                      key={e.id}
                      layout
                      initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}
                      onClick={() => flagged && navigate("/app/schedule/conflicts")}
                      style={{ top, height }}
                      className={`absolute left-0 right-2 rounded-lg px-3 py-1.5 text-left bg-gradient-to-r ${CAT_COLOR[e.category] || CAT_COLOR.General} ${flagged ? "ring-2 ring-coral-400 animate-pulse" : ""}`}
                    >
                      <p className="text-xs font-semibold truncate text-white/95">{e.task_title}</p>
                      <p className="text-[10px] text-white/70">{start.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</p>
                    </motion.button>
                  );
                })}
              </AnimatePresence>
            </div>
          </div>
        </div>
      )}

      <Outlet />
    </div>
  );
}

function AgendaCard({ entry, flagged, onClick }) {
  return (
    <button onClick={onClick} className={`w-full text-left flex items-center gap-3 p-3 rounded-lg bg-white/5 ${flagged ? "ring-1 ring-coral-400" : ""}`}>
      <div className={`w-1.5 self-stretch rounded-full bg-gradient-to-b ${CAT_COLOR[entry.category] || CAT_COLOR.General}`} />
      <div className="min-w-0 flex-1">
        <p className="text-sm font-semibold truncate">{entry.task_title}</p>
        <p className="text-xs text-slate-400">{new Date(entry.start_time).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })} · {entry.category}</p>
      </div>
      {flagged && <span className="text-coral-400 text-xs font-semibold">⚠</span>}
    </button>
  );
}
