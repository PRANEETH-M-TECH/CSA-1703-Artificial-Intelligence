import { motion } from "framer-motion";

export default function StatCard({ label, value, sub, gradient = "bg-grad-primary", delay = 0 }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.4 }}
      className="glass rounded-xl2 p-5 relative overflow-hidden"
    >
      <div className={`absolute -top-8 -right-8 w-24 h-24 rounded-full ${gradient} opacity-20 blur-xl`} />
      <p className="text-xs text-slate-400 mb-2">{label}</p>
      <p className="text-2xl font-display font-bold">{value}</p>
      {sub && <p className="text-xs text-slate-500 mt-1">{sub}</p>}
    </motion.div>
  );
}
