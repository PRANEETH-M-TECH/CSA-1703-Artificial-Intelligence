import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { ConflictsAPI } from "../api/client";
import ConflictBanner from "../components/ConflictBanner";

export default function ConflictAlerts() {
  const [conflicts, setConflicts] = useState([]);
  const [traces, setTraces] = useState({});
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const load = () => ConflictsAPI.list().then(setConflicts).finally(() => setLoading(false));
  useEffect(() => { load(); }, []);

  const expand = async (conflict) => {
    if (traces[conflict.id]) return;
    const res = await ConflictsAPI.explain(conflict.id);
    setTraces((t) => ({ ...t, [conflict.id]: res.trace }));
  };

  return (
    <div className="p-6 max-w-2xl mx-auto pb-16">
      <button onClick={() => navigate(-1)} className="text-sm text-slate-400 mb-4">‹ Back to schedule</button>
      <h1 className="text-2xl font-display font-bold mb-1">Conflict alerts</h1>
      <p className="text-slate-400 text-sm mb-6">Detected by Module 2's forward-chaining rule engine.</p>

      {loading ? (
        <div className="space-y-3">{[0, 1].map((i) => <div key={i} className="glass rounded-xl2 h-20 animate-pulse" />)}</div>
      ) : conflicts.length === 0 ? (
        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass rounded-xl2 p-10 text-center">
          <p className="text-3xl mb-2">✅</p>
          <p className="font-semibold">No conflicts right now</p>
          <p className="text-slate-400 text-sm mt-1">Your schedule is consistent.</p>
        </motion.div>
      ) : (
        <div className="space-y-3">
          <AnimatePresence>
            {conflicts.map((c) => (
              <ConflictBanner
                key={c.id}
                conflict={c}
                trace={traces[c.id]}
                onExpand={expand}
                onResolve={(conf) => navigate(`/app/schedule/conflicts/${conf.id}`)}
              />
            ))}
          </AnimatePresence>
        </div>
      )}
    </div>
  );
}
