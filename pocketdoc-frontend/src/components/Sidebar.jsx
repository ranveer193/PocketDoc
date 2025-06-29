/* Sidebar.jsx */
import { useState } from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import {
  Home,
  Clock,
  BarChart3,
  User,
  Menu as MenuIcon,
} from 'lucide-react';
import ThemeToggle from '../components/ThemeToggle';

const links = [
  { to: '/chat', icon: Home, label: 'Chat' },
  { to: '/history', icon: Clock, label: 'History' },
  { to: '/analytics', icon: BarChart3, label: 'Analytics' },
  { to: '/profile', icon: User, label: 'Profile' },
];

export default function Sidebar() {
  const { pathname } = useLocation();
  const [open, setOpen] = useState(false);

  /* ───────────────────────── Link group ───────────────────────── */
  const LinkGroup = () => (
    <nav className="flex flex-col gap-2 p-3">
      {links.map(({ to, icon: Icon, label }) => {
        const active = pathname === to;
        return (
          <NavLink
            key={to}
            to={to}
            onClick={() => setOpen(false)} // close after click
            className={`flex items-center gap-3 rounded-lg px-4 py-2 text-sm font-medium transition
              ${
                active
                  ? 'bg-blue-100 text-blue-700 dark:bg-blue-500/20 dark:text-blue-300'
                  : 'hover:bg-blue-50 dark:hover:bg-slate-800/50'
              }`}
          >
            <Icon size={18} />
            {label}
          </NavLink>
        );
      })}
    </nav>
  );

  /* ───────────────────────── Render ───────────────────────── */
  return (
    <>
      {/* ── Small‑screen floating bar (top‑right) ───────────── */}
      <div
        className="md:hidden fixed top-2 right-2 z-50 flex items-center gap-2
                   bg-white/70 dark:bg-slate-900/70 backdrop-blur-md
                   rounded-lg shadow-lg ring-1 ring-slate-200/60 dark:ring-slate-700/50
                   pl-3 pr-2 py-1"
      >
        {/* Logo first */}
        <h1 className="text-lg font-bold bg-gradient-to-r from-blue-600 to-teal-400 bg-clip-text text-transparent">
          PocketDoc
        </h1>

        {/* Menu trigger */}
        <button
          onClick={() => setOpen((p) => !p)}
          className="p-2 rounded hover:bg-slate-200/60 dark:hover:bg-slate-800/60 transition"
          aria-label="Open menu"
        >
          <MenuIcon size={20} />
        </button>

        {/* Optional Theme toggle (last) */}
        <ThemeToggle />
      </div>

      {/* Dropdown menu overlay */}
      {open && (
        <div
          className="md:hidden fixed right-2 top-[3.5rem] z-40 w-56
                     bg-white dark:bg-slate-900
                     rounded-xl shadow-xl ring-1 ring-slate-200 dark:ring-slate-800"
        >
          <LinkGroup />
        </div>
      )}

      {/* ── Desktop sidebar ─────────────────────────────────── */}
      <aside
        className="hidden md:flex flex-col h-screen w-64 p-6
                   bg-white/60 dark:bg-slate-900/70 backdrop-blur-md
                   shadow-lg ring-1 ring-slate-300/30 dark:ring-slate-700/50
                   border-r border-slate-200 dark:border-slate-800"
      >
        <h1 className="text-3xl font-extrabold mb-6 bg-gradient-to-r from-blue-600 to-teal-400 bg-clip-text text-transparent">
          PocketDoc
        </h1>

        <LinkGroup />

        <div className="mt-auto pt-4 border-t border-slate-200 dark:border-slate-700">
          <ThemeToggle />
        </div>
      </aside>
    </>
  );
}
