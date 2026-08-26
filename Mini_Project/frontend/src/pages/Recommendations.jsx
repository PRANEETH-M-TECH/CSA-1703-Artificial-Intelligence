import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence, useMotionValue, useTransform } from "framer-motion";
import { LearningAPI } from "../api/client";
import { useAuth } from "../context/AuthContext";
import { SparkleIcon, CheckIcon, CloseIcon } from "../components/Icons";

export default function Recommendations() {
  const [recs, setRecs] = useState(null);
  const [dismissed, setDismissed] = useState([]);
  const [justAccepted, setJustAccepted] = useState(null);
  const { refreshUser } = useAuth();
  const navigate = useNavigate();

  useEffect(() => { LearningAPI.recommendations().then(setRecs); }, []);

  const visible = (recs || []).filter((r) => !dismissed.includes(r.category));

  const accept = async (rec) => {
    await LearningAPI.acceptRecommendation(rec.category, rec.best_hour);
    await refreshUser?.();
    setJustAccepted(rec);
    setDismissed((d) => [...d, rec.category]);
    setTimeout(() => setJustAccepted((cur) => (cur === rec ? null : cur)), 3200);
  };

  return (
    <div className="p-6 max-w-lg mx-auto pb-16 min-h-[70vh] flex flex-col">
      <button onClick={() => navigate(-1)} className="text-sm text-slate-400 mb-4">‹ Back to insights</button>
      <div className="flex items-center gap-2 mb-1">
        <SparkleIcon className="w-5 h-5 text-amber-400" />
        <h1 className="text-2xl font-display font-bold">Recommendations</h1>
      </div>
      <p className="text-slate-400 text-sm mb-8">Swipe right to accept, left to dismiss.</p>

      <AnimatePresence>
        {justAccepted && (
          <motion.div
            initial={{ opacity: 0, y: -10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}
            className="mb-4 px-4 py-3 rounded-lg bg-mint-500/15 border border-mint-500/30 text-mint-300 text-sm"
          >
            ✓ Applied — new "{justAccepted.category}" tasks now default to {justAccepted.best_hour}:00. Module 1 will prefer this slot next time you add one.
          </motion.div>
        )}
      </AnimatePresence>

      <div className="flex-1 relative">
        {recs === null ? (
          <div className="glass rounded-xl2 h-72 animate-pulse" />
        ) : visible.length === 0 ? (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="glass rounded-xl2 p-10 text-center">
            <p className="text-3xl mb-2">🎉</p>
            <p className="font-semibold">All caught up</p>
            <p className="text-slate-400 text-sm mt-1">{recs.length === 0 ? "Log more task history to unlock recommendations." : "No more recommendations to review."}</p>
          </motion.div>
        ) : (
          <div className="relative h-72">
            <AnimatePresence>
              {visible.slice(0, 3).reverse().map((rec, idx, arr) => (
                <RecCard
                  key={rec.category}
                  rec={rec}
                  stackIndex={arr.length - 1 - idx}
                  onAccept={() => accept(rec)}
                  onDismiss={() => setDismissed((d) => [...d, rec.category])}
                />
              ))}
            </AnimatePresence>
          </div>
        )}
      </div>
    </div>
  );
}

function RecCard({ rec, stackIndex, onAccept, onDismiss }) {
  const x = useMotionValue(0);
  const rotate = useTransform(x, [-200, 200], [-12, 12]);
  const acceptOpacity = useTransform(x, [20, 120], [0, 1]);
  const dismissOpacity = useTransform(x, [-120, -20], [1, 0]);
  const isTop = stackIndex === 0;

  return (
    <motion.div
      style={{ x: isTop ? x : 0, rotate: isTop ? rotate : 0, zIndex: 10 - stackIndex }}
      className="absolute inset-0 glass rounded-xl2 p-6 flex flex-col justify-between shadow-card"
      initial={{ scale: 1 - stackIndex * 0.05, y: stackIndex * 10, opacity: 0 }}
      animate={{ scale: 1 - stackIndex * 0.05, y: stackIndex * 10, opacity: 1 }}
      exit={{ x: x.get() > 0 ? 300 : -300, opacity: 0, transition: { duration: 0.3 } }}
      drag={isTop ? "x" : false}
      dragConstraints={{ left: 0, right: 0 }}
      dragElastic={0.7}
      onDragEnd={(_, info) => {
        if (info.offset.x > 120) onAccept();
        else if (info.offset.x < -120) onDismiss();
      }}
      whileTap={isTop ? { cursor: "grabbing" } : {}}
    >
      {isTop && (
        <>
          <motion.div style={{ opacity: acceptOpacity }} className="absolute top-6 left-6 text-mint-400 font-bold text-sm border-2 border-mint-400 rounded px-2 py-0.5 -rotate-12">ACCEPT</motion.div>
          <motion.div style={{ opacity: dismissOpacity }} className="absolute top-6 right-6 text-coral-400 font-bold text-sm border-2 border-coral-400 rounded px-2 py-0.5 rotate-12">DISMISS</motion.div>
        </>
      )}
      <div>
        <span className="text-[11px] px-2.5 py-1 rounded-full bg-accent-500/20 text-accent-400 font-semibold">{rec.category}</span>
        <p className="mt-4 text-lg leading-snug font-medium">{rec.message}</p>
      </div>
      <div>
        <div className="flex items-center justify-between text-xs text-slate-400 mb-1">
          <span>Confidence</span><span>{Math.round(rec.confidence * 100)}%</span>
        </div>
        <div className="h-2 rounded-full bg-white/10 overflow-hidden">
          <motion.div initial={{ width: 0 }} animate={{ width: `${rec.confidence * 100}%` }} transition={{ duration: 0.8 }} className="h-full bg-grad-primary" />
        </div>
        {isTop && (
          <div className="flex gap-3 mt-5">
            <button onClick={onDismiss} className="flex-1 py-2.5 rounded-lg bg-white/5 flex items-center justify-center gap-1.5 text-sm">
              <CloseIcon className="w-4 h-4" /> Dismiss
            </button>
            <button onClick={onAccept} className="flex-1 py-2.5 rounded-lg bg-grad-primary flex items-center justify-center gap-1.5 text-sm font-semibold">
              <CheckIcon className="w-4 h-4" /> Accept
            </button>
          </div>
        )}
      </div>
    </motion.div>
  );
}
