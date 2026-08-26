import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { TasksAPI, ScheduleAPI, ConflictsAPI } from "../api/client";
import { useAuth } from "../context/AuthContext";
import StatCard from "../components/StatCard";
import TaskCard from "../components/TaskCard";
import { PlusIcon } from "../components/Icons";

export default function HomeDashboard() {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [tasks, setTasks] = useState([]);
  const [schedule, setSchedule] = useState([]);
  const [conflicts, setConflicts] = useState([]);
  const [fabOpen, setFabOpen] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([TasksAPI.list(), ScheduleAPI.get(), ConflictsAPI.list()])
      .then(([t, s, c]) => {
        setTasks(t);
        setSchedule(s);
        setConflicts(c);
      })
      .finally(() => setLoading(false));
  }, []);

  const today = new Date().toDateString();
  const todayEntries = schedule.filter((e) => new Date(e.start_time).toDateString() === today);
  const pending = tasks.filter((t) => t.status !== "completed");
  const hour = new Date().getHours();
  const greeting = hour < 12 ? "Good morning" : hour < 18 ? "Good afternoon" : "Good evening";

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }} className="flex items-center justify-between mb-6">
        <div>
          <p className="text-slate-400 text-sm">{greeting},</p>
          <h1 className="text-2xl font-display font-bold">{user?.name?.split(" ")[0] || "there"} 👋</h1>
        </div>
        {conflicts.length > 0 && (
          <button
            onClick={() => navigate("/app/schedule/conflicts")}
            className="relative w-11 h-11 rounded-full glass flex items-center justify-center border border-coral-500/40"
          >
            <span className="text-coral-400 text-lg">⚠</span>
            <span className="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-coral-500 text-[10px] font-bold flex items-center justify-center">
              {conflicts.length}
            </span>
          </button>
        )}
      </motion.div>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard label="Pending tasks" value={pending.length} delay={0.05} />
        <StatCard label="Today's agenda" value={todayEntries.length} sub="scheduled slots" delay={0.1} gradient="bg-grad-warm" />
        <StatCard label="Active conflicts" value={conflicts.length} delay={0.15} gradient="bg-grad-warm" />
        <StatCard label="Total tasks" value={tasks.length} delay={0.2} />
      </div>

      <div className="grid lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <div className="flex items-center justify-between mb-3">
            <h2 className="font-display font-bold">Today's agenda</h2>
            <button onClick={() => navigate("/app/schedule")} className="text-xs text-accent-400 font-semibold">View schedule</button>
          </div>
          {loading ? (
            <SkeletonList />
          ) : todayEntries.length === 0 ? (
            <EmptyState onGenerate={() => navigate("/app/schedule")} />
          ) : (
            <div className="space-y-3">
              {todayEntries.map((e, i) => (
                <motion.div key={e.id} initial={{ opacity: 0, x: -12 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.05 }}
                  className="glass rounded-xl2 p-4 flex items-center gap-4">
                  <div className="text-center shrink-0 w-14">
                    <p className="text-sm font-bold">{new Date(e.start_time).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</p>
                  </div>
                  <div className="w-1 self-stretch rounded-full bg-grad-primary" />
                  <div className="min-w-0">
                    <p className="font-semibold truncate">{e.task_title}</p>
                    <p className="text-xs text-slate-400">{e.category}</p>
                  </div>
                </motion.div>
              ))}
            </div>
          )}
        </div>

        <div>
          <h2 className="font-display font-bold mb-3">Module summary</h2>
          <div className="space-y-3">
            <ModuleWidget title="Module 1 · Scheduler" desc="CSP + A* search" stat={`${schedule.length} slots placed`} color="from-accent-500 to-mint-500" />
            <ModuleWidget title="Module 2 · Reasoning" desc="Forward/backward chaining" stat={`${conflicts.length} conflicts flagged`} color="from-coral-500 to-amber-500" />
            <ModuleWidget title="Module 3 · Learning" desc="Decision tree" stat="Personalizing your plan" color="from-accent-500 to-coral-500" />
          </div>
        </div>
      </div>

      {/* FAB */}
      <div className="fixed bottom-24 lg:bottom-8 right-6 z-30">
        <motion.button
          whileTap={{ scale: 0.9 }}
          onClick={() => navigate("/app/tasks/new")}
          className="w-14 h-14 rounded-full bg-grad-primary shadow-glow flex items-center justify-center relative"
        >
          <motion.span
            className="absolute inset-0 rounded-full bg-accent-500"
            animate={{ scale: [1, 1.6], opacity: [0.5, 0] }}
            transition={{ duration: 1.6, repeat: Infinity, ease: "easeOut" }}
          />
          <PlusIcon className="w-6 h-6 relative z-10" />
        </motion.button>
      </div>
    </div>
  );
}

function ModuleWidget({ title, desc, stat, color }) {
  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="glass rounded-xl2 p-4">
      <div className={`h-1 w-10 rounded-full bg-gradient-to-r ${color} mb-3`} />
      <p className="font-semibold text-sm">{title}</p>
      <p className="text-xs text-slate-400 mb-2">{desc}</p>
      <p className="text-xs text-slate-300">{stat}</p>
    </motion.div>
  );
}

function EmptyState({ onGenerate }) {
  return (
    <div className="glass rounded-xl2 p-8 text-center">
      <p className="text-slate-400 text-sm mb-3">Nothing scheduled for today yet.</p>
      <button onClick={onGenerate} className="px-4 py-2 rounded-lg bg-grad-primary text-sm font-semibold">Generate schedule</button>
    </div>
  );
}

function SkeletonList() {
  return (
    <div className="space-y-3">
      {[0, 1, 2].map((i) => (
        <div key={i} className="glass rounded-xl2 p-4 h-16 animate-pulse" />
      ))}
    </div>
  );
}
