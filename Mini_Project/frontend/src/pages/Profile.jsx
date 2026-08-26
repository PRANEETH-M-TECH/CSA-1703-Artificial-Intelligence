import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { useAuth } from "../context/AuthContext";
import { AuthAPI } from "../api/client";
import { LogoutIcon, UserIcon } from "../components/Icons";

export default function Profile() {
  const { user, logout, refreshUser } = useAuth();
  const navigate = useNavigate();
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [notify, setNotify] = useState(true);
  const [startHour, setStartHour] = useState(user?.work_start_hour ?? 9);
  const [endHour, setEndHour] = useState(user?.work_end_hour ?? 18);
  const [saved, setSaved] = useState(false);

  const saveHours = async () => {
    await AuthAPI.updateMe({ work_start_hour: Number(startHour), work_end_hour: Number(endHour) });
    await refreshUser();
    setSaved(true);
    setTimeout(() => setSaved(false), 1500);
  };

  const doLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="p-6 max-w-lg mx-auto pb-16">
      <h1 className="text-2xl font-display font-bold mb-6">Profile</h1>

      <div className="glass rounded-xl2 p-6 flex items-center gap-4 mb-6">
        <div className="w-16 h-16 rounded-full bg-grad-primary flex items-center justify-center shrink-0">
          <UserIcon className="w-8 h-8" />
        </div>
        <div className="min-w-0">
          <p className="font-display font-bold truncate">{user?.name}</p>
          <p className="text-slate-400 text-sm truncate">{user?.email}</p>
        </div>
      </div>

      <div className="glass rounded-xl2 p-5 mb-6">
        <h2 className="font-semibold mb-4 text-sm">Work hours (used by the scheduler)</h2>
        <div className="grid grid-cols-2 gap-3 mb-4">
          <div>
            <label className="block text-xs text-slate-400 mb-1.5">Start hour</label>
            <input type="number" min={0} max={23} value={startHour} onChange={(e) => setStartHour(e.target.value)}
              className="w-full px-4 py-2.5 rounded-lg bg-white/5 border border-white/10 outline-none focus:border-accent-500" />
          </div>
          <div>
            <label className="block text-xs text-slate-400 mb-1.5">End hour</label>
            <input type="number" min={1} max={24} value={endHour} onChange={(e) => setEndHour(e.target.value)}
              className="w-full px-4 py-2.5 rounded-lg bg-white/5 border border-white/10 outline-none focus:border-accent-500" />
          </div>
        </div>
        <button onClick={saveHours} className="w-full py-2.5 rounded-lg bg-grad-primary text-sm font-semibold">
          {saved ? "Saved ✓" : "Save"}
        </button>
      </div>

      <div className="glass rounded-xl2 p-5 mb-6 flex items-center justify-between">
        <div>
          <p className="font-semibold text-sm">Notifications</p>
          <p className="text-xs text-slate-400">Conflict + deadline alerts</p>
        </div>
        <button onClick={() => setNotify((n) => !n)}
          className={`w-12 h-7 rounded-full p-1 transition-colors ${notify ? "bg-accent-500" : "bg-white/10"}`}>
          <motion.div layout className="w-5 h-5 rounded-full bg-white" animate={{ x: notify ? 20 : 0 }} transition={{ type: "spring", stiffness: 500, damping: 30 }} />
        </button>
      </div>

      <button onClick={() => setConfirmOpen(true)}
        className="w-full py-3.5 rounded-lg bg-coral-500/15 text-coral-400 font-semibold flex items-center justify-center gap-2">
        <LogoutIcon className="w-5 h-5" /> Log out
      </button>

      <AnimatePresence>
        {confirmOpen && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-6" onClick={() => setConfirmOpen(false)}>
            <motion.div initial={{ scale: 0.85, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.85, opacity: 0 }}
              transition={{ type: "spring", stiffness: 400, damping: 28 }}
              className="glass rounded-xl2 p-6 w-full max-w-sm" onClick={(e) => e.stopPropagation()}>
              <p className="font-display font-bold text-lg mb-2">Log out?</p>
              <p className="text-slate-400 text-sm mb-6">You'll need to sign in again to access your schedule.</p>
              <div className="flex gap-3">
                <button onClick={() => setConfirmOpen(false)} className="flex-1 py-2.5 rounded-lg bg-white/5 text-sm font-semibold">Cancel</button>
                <button onClick={doLogout} className="flex-1 py-2.5 rounded-lg bg-coral-500 text-sm font-semibold">Log out</button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
