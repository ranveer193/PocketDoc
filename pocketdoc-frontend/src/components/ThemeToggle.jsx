import { useEffect, useState } from "react";
import { Sun, Moon } from "lucide-react";

export default function ThemeToggle() {
  // Figure out the initial theme in a browser-safe way
  const [dark, setDark] = useState(() => {
    if (typeof window === "undefined") return false;        // SSR safety
    return (
      localStorage.theme === "dark" ||
      (!localStorage.theme &&
        window.matchMedia("(prefers-color-scheme: dark)").matches)
    );
  });

  // Apply theme to <html> and persist
  useEffect(() => {
    const root = document.documentElement;
    root.classList.toggle("dark", dark);
    root.style.colorScheme = dark ? "dark" : "light";       // nice-to-have
    localStorage.theme = dark ? "dark" : "light";
  }, [dark]);

  // Cross‑tab sync
  useEffect(() => {
    const onStorage = (e) => {
      if (e.key === "theme") setDark(e.newValue === "dark");
    };
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);

  return (
    <button
      onClick={() => setDark(!dark)}
      className="p-2 rounded-lg bg-white/30 dark:bg-slate-800/30 shadow hover:scale-105 transition"
      title="Toggle theme"
    >
      {dark ? <Sun size={19} /> : <Moon size={19} />}
    </button>
  );
}
