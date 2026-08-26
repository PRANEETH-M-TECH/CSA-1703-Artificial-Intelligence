import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";

const SLIDES = [
  {
    title: "It schedules for you",
    body: "TaskMind searches for the best time slot for every task using CSP + A* search — balancing deadlines, priorities, and your work hours.",
    gradient: "bg-grad-primary",
    glyph: "🗓️",
  },
  {
    title: "It catches conflicts before they happen",
    body: "A rule-based reasoning engine flags overlaps and overdue tasks, then explains exactly why — with a full forward/backward-chaining trace.",
    gradient: "bg-grad-warm",
    glyph: "⚡",
  },
  {
    title: "It learns what works for you",
    body: "A decision tree studies your completion history and recommends the best time-of-day for every task category — personalized, over time.",
    gradient: "bg-grad-primary",
    glyph: "🧠",
  },
];

export default function Onboarding() {
  const [index, setIndex] = useState(0);
  const navigate = useNavigate();

  const finish = () => {
    localStorage.setItem("taskmind_seen_onboarding", "1");
    navigate("/login");
  };

  const next = () => (index < SLIDES.length - 1 ? setIndex(index + 1) : finish());

  const slide = SLIDES[index];

  return (
    <div className="min-h-screen flex flex-col p-6">
      <div className="flex justify-end">
        <button onClick={finish} className="text-sm text-slate-400 hover:text-slate-200">Skip</button>
      </div>

      <div className="flex-1 flex flex-col items-center justify-center text-center max-w-md mx-auto w-full">
        <AnimatePresence mode="wait">
          <motion.div
            key={index}
            initial={{ opacity: 0, x: 60 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -60 }}
            transition={{ duration: 0.35 }}
            className="w-full"
          >
            <div className={`w-24 h-24 mx-auto rounded-full ${slide.gradient} flex items-center justify-center text-4xl shadow-glow mb-8`}>
              {slide.glyph}
            </div>
            <h2 className="text-2xl font-display font-bold mb-3">{slide.title}</h2>
            <p className="text-slate-400 leading-relaxed">{slide.body}</p>
          </motion.div>
        </AnimatePresence>
      </div>

      <div className="flex items-center justify-center gap-2 mb-8">
        {SLIDES.map((_, i) => (
          <motion.div
            key={i}
            className="h-1.5 rounded-full bg-accent-500"
            animate={{ width: i === index ? 28 : 8, opacity: i === index ? 1 : 0.3 }}
            transition={{ duration: 0.3 }}
          />
        ))}
      </div>

      <button
        onClick={next}
        className="w-full max-w-md mx-auto py-4 rounded-xl2 bg-grad-primary font-display font-bold shadow-glow hover:opacity-90 transition-opacity"
      >
        {index < SLIDES.length - 1 ? "Next" : "Get started"}
      </button>
    </div>
  );
}
