import { Download } from 'lucide-react';

export default function PdfSummaryButton({ onClick }) {
  return (
    <button
      onClick={onClick}
      className="flex items-center gap-1 text-blue-600 dark:text-cyan-400 hover:underline text-sm"
    >
      <Download size={16} /> PDF Summary
    </button>
  );
}
