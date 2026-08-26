import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { LogoMark, CheckIcon } from "../components/Icons";
import { useAuth } from "../context/AuthContext";

export default function Signup() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [success, setSuccess] = useState(false);
  const { signup } = useAuth();
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      await signup(name, email, password);
      setSuccess(true);
      setTimeout(() => navigate("/app/home"), 900);
    } catch (err) {
      setError(err?.response?.data?.detail || "Could not create account");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <form onSubmit={submit} className="w-full max-w-sm glass rounded-xl2 p-8 relative overflow-hidden">
        <AnimatePresence>
          {success && (
            <motion.div
              initial={{ opacity: 0 }} animate={{ opacity: 1 }}
              className="absolute inset-0 z-10 bg-base-900/95 flex flex-col items-center justify-center gap-4"
            >
              <motion.div
                initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ type: "spring", stiffness: 260, damping: 18 }}
                className="w-16 h-16 rounded-full bg-mint-500/20 flex items-center justify-center"
              >
                <CheckIcon className="w-8 h-8 text-mint-400" />
              </motion.div>
              <p className="font-display font-bold">Account created!</p>
            </motion.div>
          )}
        </AnimatePresence>

        <div className="flex flex-col items-center mb-8">
          <LogoMark className="w-14 h-14 mb-3" />
          <h1 className="text-xl font-display font-bold">Create your agent</h1>
          <p className="text-slate-400 text-sm mt-1">Start scheduling smarter today</p>
        </div>

        <label className="block text-xs text-slate-400 mb-1.5">Name</label>
        <input required value={name} onChange={(e) => setName(e.target.value)}
          className="w-full mb-4 px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-accent-500 outline-none transition-colors" />

        <label className="block text-xs text-slate-400 mb-1.5">Email</label>
        <input type="email" required value={email} onChange={(e) => setEmail(e.target.value)}
          className="w-full mb-4 px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-accent-500 outline-none transition-colors" />

        <label className="block text-xs text-slate-400 mb-1.5">Password</label>
        <input type="password" required minLength={6} value={password} onChange={(e) => setPassword(e.target.value)}
          className="w-full mb-2 px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-accent-500 outline-none transition-colors" />
        {error && <p className="text-coral-400 text-sm mb-2">{error}</p>}
        <p className="text-xs text-slate-500 mb-6">At least 6 characters.</p>

        <button type="submit" disabled={busy}
          className="w-full py-3.5 rounded-lg bg-grad-primary font-display font-bold shadow-glow hover:opacity-90 transition-opacity disabled:opacity-50">
          {busy ? "Creating..." : "Sign up"}
        </button>

        <p className="text-center text-sm text-slate-400 mt-6">
          Already have an account? <Link to="/login" className="text-accent-400 font-semibold hover:underline">Sign in</Link>
        </p>
      </form>
    </div>
  );
}
