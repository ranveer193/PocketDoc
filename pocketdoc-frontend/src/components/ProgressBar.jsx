export default function ProgressBar({ progress }) {
  return (
    <div className="w-full h-1 bg-slate-200 dark:bg-slate-700 rounded overflow-hidden">
      <div
        className="h-full bg-primary-600 transition-all duration-300"
        style={{ width: `${progress}%` }}
      />
    </div>
  );
}
