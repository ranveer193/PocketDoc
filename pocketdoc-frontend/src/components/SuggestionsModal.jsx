import { useEffect } from 'react';
import DiseaseResults from './DiseaseResults';
import { X } from 'lucide-react';

export default function SuggestionsModal({ open, onClose, preds, followup, finished, onFacts }) {
  /* lock body scroll */
  useEffect(() => { document.body.style.overflow = open ? 'hidden' : 'auto'; }, [open]);
  if (!open) return null;

  return (
    /* ‣ click backdrop to close */
    <div
      className="fixed inset-0 z-40 flex items-center justify-center bg-black/50 backdrop-blur-sm"
      onClick={onClose}
    >
      {/* ‣ stop click bubbling inside card */}
      <div
        onClick={e => e.stopPropagation()}
        className="bg-white dark:bg-slate-800 rounded-lg shadow-xl max-w-lg w-full mx-4 p-6 animate-[fadeIn_0.25s_ease]"
      >
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-slate-400 hover:text-slate-600"
        >
          <X size={20} />
        </button>

        <h2 className="text-lg font-semibold mb-4 text-primary-600">
          AI Suggestions
        </h2>

        <DiseaseResults data={preds} />

        {followup && (
          <div className="mt-4 italic text-sm text-slate-700 dark:text-slate-300">
            {followup}
          </div>
        )}

        {finished && (
          <button
            onClick={() => { onFacts(); onClose(); }}
            className="mt-6 w-full bg-amber-600 hover:bg-amber-700 text-white rounded-lg py-2 transition"
          >
            Tell me more about this diagnosis
          </button>
        )}
      </div>
    </div>
  );
}
