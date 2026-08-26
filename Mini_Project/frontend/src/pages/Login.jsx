import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { LogoMark } from "../components/Icons";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const [email, setEmail] = useState("demo@taskmind.app");
  const [password, setPassword] = useState("demo1234");
  const [error, setError] = useState("");
  const [shake, setShake] = useState(0);
  const [busy, setBusy] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    setBusy(true);
    setError("");
    try {
      await login(email, password);
      navigate("/app/home");
    } catch (err) {
      setError(err?.response?.data?.detail || "Invalid credentials");
      setShake((s) => s + 1);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-6">
      <motion.form
        onSubmit={submit}
        key={shake}
        animate={shake ? { x: [0, -10, 10, -8, 8, -4, 4, 0] } : {}}
        transition={{ duration: 0.4 }}
        className="w-full max-w-sm glass rounded-xl2 p-8"
      >
        <div className="flex flex-col items-center mb-8">
          <LogoMark className="w-14 h-14 mb-3" />
          <h1 className="text-xl font-display font-bold">Welcome back</h1>
          <p className="text-slate-400 text-sm mt-1">Sign in to your TaskMind agent</p>
        </div>

        <label className="block text-xs text-slate-400 mb-1.5">Email</label>
        <input
          type="email" required value={email} onChange={(e) => setEmail(e.target.value)}
          className="w-full mb-4 px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-accent-500 outline-none transition-colors"
        />
        <label className="block text-xs text-slate-400 mb-1.5">Password</label>
        <input
          type="password" required value={password} onChange={(e) => setPassword(e.target.value)}
          className="w-full mb-2 px-4 py-3 rounded-lg bg-white/5 border border-white/10 focus:border-accent-500 outline-none transition-colors"
        />
        {error && <p className="text-coral-400 text-sm mb-2">{error}</p>}
        <p className="text-xs text-slate-500 mb-6">Demo account prefilled — just hit sign in.</p>

        <button
          type="submit" disabled={busy}
          className="w-full py-3.5 rounded-lg bg-grad-primary font-display font-bold shadow-glow hover:opacity-90 transition-opacity disabled:opacity-50"
        >
          {busy ? "Signing in..." : "Sign in"}
        </button>

        <p className="text-center text-sm text-slate-400 mt-6">
          New here? <Link to="/signup" className="text-accent-400 font-semibold hover:underline">Create an account</Link>
        </p>
      </motion.form>
    </div>
  );
}
