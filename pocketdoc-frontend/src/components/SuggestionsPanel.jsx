import { useState } from 'react';
import DiseaseResults from './DiseaseResults';

export default function SuggestionsPanel({ preds, followup }) {
  const [open, setOpen] = useState(false);

  if (!preds?.length) return null;

  return (
    <div className="mt-2">
      <button
        onClick={()=>setOpen(o=>!o)}
        className="px-4 py-2 bg-amber-500 hover:bg-amber-600 text-white rounded-full shadow transition"
      >
        {open ? 'Hide suggestions' : 'View suggestions'}
      </button>

      {open && (
        <div className="mt-3 space-y-4 animate-[fadeIn_0.25s_ease]">
          <DiseaseResults data={preds} />
          {followup && (
            <div className="italic text-sm text-slate-700 dark:text-slate-300">
              {followup}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
