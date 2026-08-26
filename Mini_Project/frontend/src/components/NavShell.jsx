import { NavLink, Outlet } from "react-router-dom";
import { motion } from "framer-motion";
import {
  HomeIcon, ListIcon, CalendarIcon, ChartIcon, UserIcon, LogoMark,
} from "./Icons";
import { useAuth } from "../context/AuthContext";

const NAV_ITEMS = [
  { to: "/app/home", label: "Home", Icon: HomeIcon },
  { to: "/app/tasks", label: "Tasks", Icon: ListIcon },
  { to: "/app/schedule", label: "Schedule", Icon: CalendarIcon },
  { to: "/app/insights", label: "Insights", Icon: ChartIcon },
  { to: "/app/profile", label: "Profile", Icon: UserIcon },
];

export default function NavShell() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen flex flex-col lg:flex-row">
      {/* Desktop sidebar */}
      <aside className="hidden lg:flex lg:flex-col w-64 shrink-0 glass border-r border-white/5 p-6 gap-8 sticky top-0 h-screen">
        <div className="flex items-center gap-2">
          <LogoMark />
          <span className="font-display font-bold text-lg tracking-tight">TaskMind</span>
        </div>
        <nav className="flex flex-col gap-1">
          {NAV_ITEMS.map(({ to, label, Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-xl2 transition-colors ${
                  isActive
                    ? "bg-accent-500/15 text-accent-400 font-semibold"
                    : "text-slate-400 hover:bg-white/5 hover:text-slate-200"
                }`
              }
            >
              <Icon className="w-5 h-5" />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>
        <div className="mt-auto glass rounded-xl2 p-4">
          <p className="text-xs text-slate-400 mb-1">Signed in as</p>
          <p className="font-semibold truncate">{user?.name}</p>
        </div>
      </aside>

      {/* Main content */}
      <main className="flex-1 pb-24 lg:pb-0 min-w-0">
        <Outlet />
      </main>

      {/* Mobile bottom tab bar */}
      <nav className="lg:hidden fixed bottom-0 left-0 right-0 z-40 glass border-t border-white/5 px-2 pt-2 pb-[calc(0.5rem+env(safe-area-inset-bottom))]">
        <div className="flex justify-between">
          {NAV_ITEMS.map(({ to, label, Icon }) => (
            <NavLink
              key={to}
              to={to}
              className="relative flex-1 flex flex-col items-center gap-1 py-1.5 text-[11px]"
            >
              {({ isActive }) => (
                <>
                  {isActive && (
                    <motion.div
                      layoutId="tab-pill"
                      className="absolute -top-2 w-8 h-1 rounded-full bg-accent-500"
                      transition={{ type: "spring", stiffness: 500, damping: 35 }}
                    />
                  )}
                  <Icon className={`w-5 h-5 ${isActive ? "text-accent-400" : "text-slate-500"}`} />
                  <span className={isActive ? "text-accent-400 font-semibold" : "text-slate-500"}>{label}</span>
                </>
              )}
            </NavLink>
          ))}
        </div>
      </nav>
    </div>
  );
}
