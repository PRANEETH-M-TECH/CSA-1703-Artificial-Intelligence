import { useEffect, useState } from "react";
import { useNavigate, useParams, useOutletContext } from "react-router-dom";
import Sheet from "../components/Sheet";
import { TasksAPI } from "../api/client";
import { useAuth } from "../context/AuthContext";
import { TrashIcon } from "../components/Icons";

const CATEGORIES = ["Study", "Work", "Fitness", "Personal", "Meeting", "General"];

function toLocalInputValue(iso) {
  const d = iso ? new Date(iso) : new Date(Date.now() + 3600_000);
  const pad = (n) => String(n).padStart(2, "0");
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}T${pad(d.getHours())}:${pad(d.getMinutes())}`;
}

// Applies Module 3's accepted preferred hour (from the Recommendations screen)
// to a deadline's time-of-day, keeping the date, pushing to tomorrow if that
// hour has already passed today.
function withPreferredHour(localValue, hour) {
  const d = new Date(localValue);
  d.setHours(hour, 0, 0, 0);
  if (d.getTime() <= Date.now()) d.setDate(d.getDate() + 1);
  return toLocalInputValue(d.toISOString());
}

export default function AddEditTask() {
  const { id } = useParams();
  const isEdit = Boolean(id);
  const navigate = useNavigate();
  const { reload } = useOutletContext() || {};
  const { user } = useAuth();
  const preferredHours = user?.preferred_hours || {};

  const [form, setForm] = useState({
    title: "", category: "Study", deadline: toLocalInputValue(), duration_minutes: 60, priority: 2, notes: "",
  });
  const [busy, setBusy] = useState(false);
  const [appliedHint, setAppliedHint] = useState(false);

  const handleCategoryChange = (category) => {
    setForm((f) => {
      const next = { ...f, category };
      const hour = preferredHours[category];
      if (!isEdit && hour != null) {
        next.deadline = withPreferredHour(f.deadline, hour);
        setAppliedHint(true);
      } else {
        setAppliedHint(false);
      }
      return next;
    });
  };

  useEffect(() => {
    if (isEdit) {
      TasksAPI.list().then((tasks) => {
        const t = tasks.find((x) => String(x.id) === id);
        if (t) setForm({ ...t, deadline: toLocalInputValue(t.deadline) });
      });
    }
  }, [id, isEdit]);

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    const payload = { ...form, deadline: new Date(form.deadline).toISOString(), duration_minutes: Number(form.duration_minutes), priority: Number(form.priority) };
    try {
      if (isEdit) await TasksAPI.update(id, payload);
      else await TasksAPI.create(payload);
      reload?.();
      navigate("/app/tasks");
    } finally {
      setBusy(false);
    }
  };

  const remove = async () => {
    await TasksAPI.remove(id);
    reload?.();
    navigate("/app/tasks");
  };

  return (
    <Sheet title={isEdit ? "Edit task" : "New task"} onCloseTo="/app/tasks">
      <form onSubmit={submit} className="space-y-4">
        <div>
          <label className="block text-xs text-slate-400 mb-1.5">Title</label>
          <input required value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })}
            className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-accent-500 outline-none" />
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-xs text-slate-400 mb-1.5">Category</label>
            <select value={form.category} onChange={(e) => handleCategoryChange(e.target.value)}
              className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-accent-500 outline-none">
              {CATEGORIES.map((c) => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          <div>
            <label className="block text-xs text-slate-400 mb-1.5">Priority</label>
            <select value={form.priority} onChange={(e) => setForm({ ...form, priority: Number(e.target.value) })}
              className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-accent-500 outline-none">
              <option value={1}>Low</option>
              <option value={2}>Medium</option>
              <option value={3}>High</option>
            </select>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-xs text-slate-400 mb-1.5">Deadline</label>
            <input type="datetime-local" required value={form.deadline}
              onChange={(e) => { setForm({ ...form, deadline: e.target.value }); setAppliedHint(false); }}
              className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-accent-500 outline-none" />
            {appliedHint && (
              <p className="text-[11px] text-mint-400 mt-1.5">
                ✓ Module 3 suggested {preferredHours[form.category]}:00 for {form.category} — applied
              </p>
            )}
          </div>
          <div>
            <label className="block text-xs text-slate-400 mb-1.5">Duration (min)</label>
            <input type="number" min={15} step={15} required value={form.duration_minutes}
              onChange={(e) => setForm({ ...form, duration_minutes: e.target.value })}
              className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-accent-500 outline-none" />
          </div>
        </div>

        <div>
          <label className="block text-xs text-slate-400 mb-1.5">Notes</label>
          <textarea value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} rows={3}
            className="w-full px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-accent-500 outline-none resize-none" />
        </div>

        <div className="flex gap-3 pt-2">
          {isEdit && (
            <button type="button" onClick={remove} className="px-4 py-3.5 rounded-lg bg-coral-500/15 text-coral-400">
              <TrashIcon className="w-5 h-5" />
            </button>
          )}
          <button type="submit" disabled={busy} className="flex-1 py-3.5 rounded-lg bg-grad-primary font-display font-bold shadow-glow disabled:opacity-50">
            {busy ? "Saving..." : isEdit ? "Save changes" : "Add task"}
          </button>
        </div>
      </form>
    </Sheet>
  );
}
