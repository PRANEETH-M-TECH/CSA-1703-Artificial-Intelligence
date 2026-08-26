import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { LogoMark } from "../components/Icons";
import { useAuth } from "../context/AuthContext";

export default function Splash() {
  const navigate = useNavigate();
  const { user, loading } = useAuth();

  useEffect(() => {
    if (loading) return;
    const t = setTimeout(() => {
      if (user) navigate("/app/home", { replace: true });
      else if (!localStorage.getItem("taskmind_seen_onboarding")) navigate("/onboarding", { replace: true });
      else navigate("/login", { replace: true });
    }, 1400);
    return () => clearTimeout(t);
  }, [loading, user, navigate]);

  return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.6 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.9, ease: "easeOut" }}
      >
        <LogoMark className="w-20 h-20" />
      </motion.div>
      <motion.h1
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.6 }}
        className="text-3xl font-display font-extrabold tracking-tight"
      >
        TaskMind
      </motion.h1>
      <motion.p
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.7, duration: 0.6 }}
        className="text-slate-400 text-sm"
      >
        Perceive · Reason · Act · Learn
      </motion.p>
    </div>
  );
}
