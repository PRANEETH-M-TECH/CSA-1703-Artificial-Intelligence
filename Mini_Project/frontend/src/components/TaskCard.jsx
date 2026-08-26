import { motion, useMotionValue, useTransform } from "framer-motion";
import { CheckIcon, TrashIcon } from "./Icons";

const PRIORITY_STYLE = {
  1: { label: "Low", cls: "bg-slate-500/20 text-slate-300" },
  2: { label: "Medium", cls: "bg-amber-500/20 text-amber-400" },
  3: { label: "High", cls: "bg-coral-500/20 text-coral-400" },
};

export default function TaskCard({ task, onClick, onComplete, onDelete }) {
  const x = useMotionValue(0);
  const completeOpacity = useTransform(x, [0, 90], [0, 1]);
  const deleteOpacity = useTransform(x, [-90, 0], [1, 0]);
  const priority = PRIORITY_STYLE[task.priority] || PRIORITY_STYLE[2];
  const overdue = task.status !== "completed" && new Date(task.deadline) < new Date();

  return (
    <div className="relative">
      <div className="absolute inset-0 flex items-center justify-between px-5 rounded-xl2 overflow-hidden">
        <motion.div style={{ opacity: completeOpacity }} className="flex items-center gap-2 text-mint-400 font-semibold">
          <CheckIcon className="w-5 h-5" /> Complete
        </motion.div>
        <motion.div style={{ opacity: deleteOpacity }} className="flex items-center gap-2 text-coral-400 font-semibold">
          Delete <TrashIcon className="w-5 h-5" />
        </motion.div>
      </div>
      <motion.div
        drag="x"
        dragConstraints={{ left: 0, right: 0 }}
        dragElastic={0.6}
        style={{ x }}
        onDragEnd={(_, info) => {
          if (info.offset.x > 100) onComplete?.(task);
          else if (info.offset.x < -100) onDelete?.(task);
        }}
        whileTap={{ scale: 0.99 }}
        onClick={() => onClick?.(task)}
        className={`relative glass rounded-xl2 p-4 flex items-center justify-between gap-4 cursor-pointer hover:border-accent-500/40 transition-colors ${
          task.status === "completed" ? "opacity-50" : ""
        }`}
      >
        <div className="min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <p className="font-semibold truncate">{task.title}</p>
            {overdue && <span className="text-[10px] px-2 py-0.5 rounded-full bg-coral-500/20 text-coral-400 font-semibold">OVERDUE</span>}
          </div>
          <div className="flex items-center gap-2 mt-1.5 text-xs text-slate-400">
            <span className="px-2 py-0.5 rounded-full bg-white/5">{task.category}</span>
            <span>{task.duration_minutes}m</span>
            <span>· {new Date(task.deadline).toLocaleString(undefined, { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" })}</span>
          </div>
        </div>
        <span className={`text-[11px] px-2.5 py-1 rounded-full font-semibold shrink-0 ${priority.cls}`}>{priority.label}</span>
      </motion.div>
    </div>
  );
}
