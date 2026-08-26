import { useEffect, useState } from "react";
import { useNavigate, Outlet } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import { TasksAPI, LearningAPI } from "../api/client";
import TaskCard from "../components/TaskCard";
import { PlusIcon } from "../components/Icons";

const FILTERS = ["All", "Pending", "Scheduled", "Completed"];
const SORTS = ["Deadline", "Priority"];

export default function TaskList() {
  const [tasks, setTasks] = useState([]);
  const [filter, setFilter] = useState("All");
  const [sort, setSort] = useState("Deadline");
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const load = () => TasksAPI.list().then(setTasks).finally(() => setLoading(false));
  useEffect(() => { load(); }, []);

  const complete = async (task) => {
    setTasks((prev) => prev.map((t) => (t.id === task.id ? { ...t, status: "completed" } : t)));
    await TasksAPI.update(task.id, { status: "completed" });
    const scheduledHour = new Date(task.deadline).getHours();
    await LearningAPI.logHistory({
      task_id: task.id, task_type: task.category, time_of_day: scheduledHour,
      planned_duration: task.duration_minutes, actual_duration: task.duration_minutes, completed_on_time: true,
    }).catch(() => {});
  };

  const remove = async (task) => {
    setTasks((prev) => prev.filter((t) => t.id !== task.id));
    await TasksAPI.remove(task.id);
  };

  let visible = tasks.filter((t) => {
    if (filter === "All") return true;
    if (filter === "Pending") return t.status === "pending";
    if (filter === "Scheduled") return t.status === "scheduled";
    if (filter === "Completed") return t.status === "completed";
    return true;
  });
  visible = [...visible].sort((a, b) =>
    sort === "Deadline" ? new Date(a.deadline) - new Date(b.deadline) : b.priority - a.priority
  );

  return (
    <div className="p-6 max-w-3xl mx-auto pb-28">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-display font-bold">Tasks</h1>
        <button onClick={() => navigate("/app/tasks/new")} className="hidden sm:flex items-center gap-1.5 px-4 py-2 rounded-lg bg-grad-primary text-sm font-semibold">
          <PlusIcon className="w-4 h-4" /> New task
        </button>
      </div>

      <div className="flex gap-2 mb-3 overflow-x-auto no-scrollbar pb-1">
        {FILTERS.map((f) => (
          <button key={f} onClick={() => setFilter(f)}
            className={`px-3.5 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-colors ${
              filter === f ? "bg-accent-500 text-white" : "bg-white/5 text-slate-400 hover:bg-white/10"
            }`}>
            {f}
          </button>
        ))}
        <div className="w-px bg-white/10 mx-1" />
        {SORTS.map((s) => (
          <button key={s} onClick={() => setSort(s)}
            className={`px-3.5 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition-colors ${
              sort === s ? "bg-mint-500/30 text-mint-400" : "bg-white/5 text-slate-400 hover:bg-white/10"
            }`}>
            Sort: {s}
          </button>
        ))}
      </div>

      {loading ? (
        <div className="space-y-3 mt-4">{[0, 1, 2, 3].map((i) => <div key={i} className="glass rounded-xl2 h-20 animate-pulse" />)}</div>
      ) : visible.length === 0 ? (
        <div className="glass rounded-xl2 p-10 text-center text-slate-400 mt-6">No tasks in this view.</div>
      ) : (
        <div className="space-y-3 mt-4">
          <AnimatePresence>
            {visible.map((task) => (
              <motion.div key={task.id} layout exit={{ opacity: 0, height: 0, marginBottom: 0 }}>
                <TaskCard
                  task={task}
                  onClick={() => navigate(`/app/tasks/${task.id}/edit`)}
                  onComplete={complete}
                  onDelete={remove}
                />
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      )}

      <button onClick={() => navigate("/app/tasks/new")}
        className="sm:hidden fixed bottom-24 right-6 w-14 h-14 rounded-full bg-grad-primary shadow-glow flex items-center justify-center z-30">
        <PlusIcon className="w-6 h-6" />
      </button>

      <Outlet context={{ reload: load }} />
    </div>
  );
}
