import ReactMarkdown from 'react-markdown';
import remarkGfm     from 'remark-gfm';
import rehypeRaw     from 'rehype-raw';

export default function ChatMessage({ role, content }) {
  const isUser = role === 'user';

  const md = (
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[rehypeRaw]}
      components={{
        a: ({ node, ...props }) => (
          <a {...props} target="_blank" rel="noopener noreferrer" className="text-primary-600 underline" />
        ),
      }}
    >
      {content}
    </ReactMarkdown>
  );

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} w-full animate-[fadeIn_0.25s_ease]`}>
      {/* triangle */}
      <div
        className={`
          relative max-w-[75%] md:max-w-[65%] lg:max-w-[55%]
          ${isUser ? 'self-end' : 'self-start'}
        `}
      >
        <div
          className={`
            px-4 py-2 rounded-2xl shadow
            ${isUser
              ? 'bg-gray-200 text-black dark:bg-gray-700 dark:text-white rounded-br-none'
              : 'bg-slate-200 dark:bg-slate-700 text-slate-900 dark:text-slate-100 rounded-bl-none'}
          `}
        >
          {isUser ? content : md}
        </div>

        {/* little tail */}
        <span
          className={`
            absolute top-0
            ${isUser
              ? '-right-2 w-0 h-0 border-t-8 border-l-8 border-t-transparent border-l-primary-600'
              : '-left-2 w-0 h-0 border-t-8 border-r-8 border-t-transparent border-r-slate-200 dark:border-r-slate-700'}
          `}
        />
      </div>
    </div>
  );
}
