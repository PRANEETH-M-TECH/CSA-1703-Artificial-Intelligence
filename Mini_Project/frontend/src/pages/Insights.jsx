import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid,
  PieChart, Pie, Cell, Legend,
} from "recharts";
import { LearningAPI } from "../api/client";
import StatCard from "../components/StatCard";
import { SparkleIcon } from "../components/Icons";

const COLORS = ["#7c5cff", "#38e0c0", "#ff6b81", "#ffb454", "#6a3ffa"];

export default function Insights() {
  const [data, setData] = useState(null);
  const navigate = useNavigate();

  useEffect(() => { LearningAPI.insights().then(setData); }, []);

  if (!data) {
    return <div className="p-6 max-w-4xl mx-auto"><div className="glass rounded-xl2 h-64 animate-pulse" /></div>;
  }

  const byCategory = Object.entries(data.by_category).map(([name, value]) => ({ name, value }));
  const byHour = Object.entries(data.by_hour)
    .map(([hour, value]) => ({ hour: `${hour}h`, hourNum: Number(hour), value }))
    .sort((a, b) => a.hourNum - b.hourNum);

  return (
    <div className="p-6 max-w-4xl mx-auto pb-16">
      <div className="flex items-center justify-between mb-1">
        <h1 className="text-2xl font-display font-bold">Insights</h1>
        <button onClick={() => navigate("/app/insights/recommendations")}
          className="flex items-center gap-1.5 px-4 py-2 rounded-lg bg-grad-warm text-sm font-semibold">
          <SparkleIcon className="w-4 h-4" /> Recommendations
        </button>
      </div>
      <p className="text-slate-400 text-sm mb-2">Module 3's decision tree, trained on your completion history.</p>
      <p className="text-[11px] text-amber-400/80 mb-6">Populated from seeded demo history for illustration — log real task completions to personalize it further.</p>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard label="Total tasks" value={data.total_tasks} delay={0} />
        <StatCard label="Completion rate" value={`${data.completion_rate}%`} gradient="bg-grad-warm" delay={0.05} />
        <StatCard label="Overdue" value={data.overdue_tasks} delay={0.1} />
        <StatCard label="Model accuracy" value={data.model_accuracy ? `${Math.round(data.model_accuracy * 100)}%` : "—"} sub="held-out test split" gradient="bg-grad-warm" delay={0.15} />
      </div>

      <div className="grid lg:grid-cols-2 gap-6">
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 }} className="glass rounded-xl2 p-5">
          <h2 className="font-display font-bold mb-4 text-sm">On-time completion by category</h2>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie data={byCategory} dataKey="value" nameKey="name" innerRadius={55} outerRadius={90} paddingAngle={3} animationDuration={900}>
                {byCategory.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
              </Pie>
              <Tooltip contentStyle={{ background: "#12131f", border: "1px solid #33354d", borderRadius: 8 }} formatter={(v) => `${v}%`} />
              <Legend wrapperStyle={{ fontSize: 11 }} />
            </PieChart>
          </ResponsiveContainer>
        </motion.div>

        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }} className="glass rounded-xl2 p-5">
          <h2 className="font-display font-bold mb-4 text-sm">Productivity by time-of-day</h2>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={byHour}>
              <CartesianGrid strokeDasharray="3 3" stroke="#24263a" />
              <XAxis dataKey="hour" tick={{ fontSize: 10, fill: "#8890b0" }} />
              <YAxis tick={{ fontSize: 10, fill: "#8890b0" }} unit="%" />
              <Tooltip contentStyle={{ background: "#12131f", border: "1px solid #33354d", borderRadius: 8 }} formatter={(v) => `${v}%`} />
              <Bar dataKey="value" fill="#7c5cff" radius={[6, 6, 0, 0]} animationDuration={900} />
            </BarChart>
          </ResponsiveContainer>
        </motion.div>
      </div>
    </div>
  );
}
