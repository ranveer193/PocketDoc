export default function TypingIndicator() {
  return (
    <div className="flex justify-start w-full animate-[fadeIn_0.3s_ease]">
      <div className="bg-slate-200 dark:bg-slate-700 rounded-2xl rounded-bl-none px-3 py-2 shadow max-w-xs">
        <div className="flex gap-1">
          <div className="h-2 w-2 bg-slate-500 rounded-full animate-bounce [animation-delay:.0s]" />
          <div className="h-2 w-2 bg-slate-500 rounded-full animate-bounce [animation-delay:.15s]" />
          <div className="h-2 w-2 bg-slate-500 rounded-full animate-bounce [animation-delay:.3s]" />
        </div>
      </div>
    </div>
  );
}
