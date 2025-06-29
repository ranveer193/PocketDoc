import { useState, useRef, useEffect } from 'react';
import { ArrowUp } from 'lucide-react';
import ChatMessage from '../components/ChatMessage';
import TypingIndicator from '../components/TypingIndicator';
import SuggestionsModal from '../components/SuggestionsModal';
import ProgressBar from '../components/ProgressBar';
import { backend } from '../api/backend';

export default function Chat() {
  const [input, setInput] = useState('');
  const [messages, setMsgs] = useState([
    { role: 'ai', content: '👋 **Hi!** How can I help you today? You can describe how you’re feeling.' },
  ]);
  const [progress, setProg] = useState(0);
  const [chatId, setChatId] = useState(null);

  const [preds, setPreds] = useState(null);
  const [followUp, setFollowUp] = useState(null);
  const [facts, setFacts] = useState(null);
  const [modalOpen, setModal] = useState(false);
  const [aiTyping, setTyping] = useState(false);

  const bottomRef = useRef(null);
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, aiTyping]);

  const push = (role, content) =>
    setMsgs((m) => [...m, { role, content }]);

  async function send() {
    if (!input.trim()) return;

    const userTxt = input;
    push('user', userTxt);
    setInput('');
    setProg(15);
    setTyping(true);              // show typing dots

    try {
      const endpoint = chatId ? '/chat/continue' : '/chat/start';
      const payload = chatId ? { chat_id: chatId, user: userTxt } : { user: userTxt };
      const { data } = await backend.post(endpoint, payload);

      setChatId(data.chat_id);
      setPreds(data.predictions || []);
      setFollowUp(data.finished ? null : data.question || null);
      setFacts(data.facts || null);

      /* Craft AI bubble text */
      let aiText;
      if (data.predictions?.length) {
        aiText = data.finished
          ? '✅ I have a likely diagnosis. Tap **View Suggestions** to see details.'
          : `Here are a few possibilities. Tap **View Suggestions** and answer me so I can narrow it down.\n\n**Follow‑up:** ${data.question}`;
      } else {
        aiText = data.question || 'Could you share some symptoms so I can assist?';
      }

      push('ai', aiText);
    } catch (err) {
      console.error(err);
      push('ai', '⚠️ Error reaching the server. Please try again.');
    } finally {
      setTyping(false);
      setProg(100);
      setTimeout(() => setProg(0), 300);
    }
  }

  const onFacts = () => {
    if (facts) push('ai', `💡 **More info:**\n\n${facts}`);
    setModal(false);
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-sky-50 to-emerald-100 dark:from-slate-800 dark:to-slate-900">
      {progress > 0 && <ProgressBar progress={progress} />}

      <main className="flex-1 overflow-y-auto px-4 py-6 md:px-8 md:py-8">
        <div className="max-w-2xl mx-auto space-y-2">
          {messages.map((m, i) => <ChatMessage key={i} {...m} />)}
          {aiTyping && <TypingIndicator />}
          <div ref={bottomRef} />
        </div>
      </main>

      {/* Suggestions modal */}
      <SuggestionsModal
        open={modalOpen}
        onClose={() => setModal(false)}
        preds={preds}
        followup={followUp}
        finished={Boolean(facts)}
        onFacts={onFacts}
      />

      <footer className="sticky bottom-0 w-full bg-white/80 dark:bg-slate-800/70 backdrop-blur-lg ring-1 ring-black/5 shadow">
        <div className="max-w-2xl mx-auto flex items-center gap-3 px-4 py-3">
          <input
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => e.key === 'Enter' && send()}
            placeholder="Describe your symptoms…"
            className="flex-1 bg-transparent outline-none placeholder-slate-500 dark:placeholder-slate-400 text-sm py-2"
          />
          <button
            onClick={send}
            disabled={!input.trim()}
            className="inline-flex items-center justify-center bg-primary-600 hover:bg-primary-700 disabled:bg-primary-600/50 text-white rounded-full h-10 w-10 transition"
          >
            <ArrowUp size={18} className="-rotate-45" />
          </button>

          {/* Launch suggestions if predictions exist */}
          {preds?.length > 0 && (
            <button
              onClick={() => setModal(true)}
              className="ml-1 text-primary-600 hover:text-primary-700 text-sm underline"
            >
              View Suggestions
            </button>
          )}
        </div>
      </footer>
    </div>
  );
}
