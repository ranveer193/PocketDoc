import { useState } from "react";
import { SYMPTOMS } from "./symptoms";
import { X, Check } from "lucide-react";

const API = import.meta.env.VITE_API_URL + "/predict";

export default function App() {
  const [query, setQuery]   = useState("");
  const [picked, setPicked] = useState([]);
  const [top, setTop]       = useState([]);
  const [suggest, setSuggest] = useState([]);
  const [loading, setLoading] = useState(false);

  const hits = query
    ? SYMPTOMS.filter(
        s => s.includes(query.toLowerCase()) && !picked.includes(s)
      ).slice(0, 8)
    : [];

  const add = s => { setPicked(p => [...p, s]); setQuery(""); };
  const remove = s => setPicked(p => p.filter(x => x !== s));

  async function predict() {
    if (!picked.length) return alert("Pick symptoms first");
    setLoading(true);
    try {
      const res = await fetch(API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symptoms: picked })
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Server error");
      setTop(data.top);
      setSuggest(data.suggest);
    } catch (e) {
      alert(e.message);
    }
    setLoading(false);
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-green-100 text-gray-800 flex flex-col items-center justify-start">
      <header className="bg-green-700 w-full text-white text-center py-5 shadow-lg">
        <h1 className="text-4xl font-bold tracking-wide">PocketDoc</h1>
        <p className="text-sm mt-1 text-green-100">AI Symptom Checker</p>
      </header>

      <main className="w-full max-w-xl px-6 py-8">
        <section className="bg-white rounded-2xl shadow-lg p-6 mb-6">
          <label htmlFor="sym" className="block font-semibold text-lg text-green-700 mb-1">
            Type a symptom
          </label>
          <input
            id="sym"
            value={query}
            onChange={e => setQuery(e.target.value)}
            className="w-full border-2 border-green-300 rounded-md p-3 focus:outline-none focus:ring-2 focus:ring-green-500"
            placeholder="e.g. headache"
            autoComplete="off"
          />
          {hits.length > 0 && (
            <div className="border rounded-md mt-1 bg-white shadow max-h-48 overflow-y-auto z-10">
              {hits.map(h => (
                <div
                  key={h}
                  className="px-3 py-2 hover:bg-green-100 cursor-pointer"
                  onClick={() => add(h)}
                >
                  {h}
                </div>
              ))}
            </div>
          )}
          <div className="flex flex-wrap gap-2 mt-4">
            {picked.map(p => (
              <span key={p} className="bg-green-600 text-white px-3 py-1 rounded-full flex items-center gap-2 text-sm shadow-sm">
                {p}
                <X size={14} className="cursor-pointer hover:text-red-200" onClick={() => remove(p)} />
              </span>
            ))}
          </div>

          <button
            disabled={loading}
            onClick={predict}
            className="mt-5 w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 rounded-lg transition duration-200 disabled:opacity-50"
          >
            {loading ? "Predicting…" : "Predict"}
          </button>
        </section>

        {top.length > 0 && (
          <section className="bg-white rounded-2xl shadow-lg p-6">
            <h3 className="text-xl font-bold mb-4 text-green-700 flex items-center gap-2">
              <Check size={20} /> Top Predictions
            </h3>
            {top.map(t => (
              <div key={t.disease} className="mb-4">
                <div className="flex justify-between text-sm font-medium mb-1">
                  <span>{t.disease}</span>
                  <span>{t.prob.toFixed(1)}%</span>
                </div>
                <div className="w-full h-3 bg-green-100 rounded">
                  <div
                    className="h-full bg-green-500 rounded transition-all duration-500"
                    style={{ width: `${t.prob}%` }}
                  />
                </div>
              </div>
            ))}
            <h4 className="mt-6 font-semibold text-green-600 mb-2">Add more symptoms:</h4>
            <ul className="list-disc list-inside text-sm text-gray-700">
              {suggest.map(s => <li key={s}>{s}</li>)}
            </ul>
          </section>
        )}
      </main>

      <footer className="text-center text-xs text-gray-500 py-6">
        © 2025 PocketDoc — For educational use only
      </footer>
    </div>
  );
}
