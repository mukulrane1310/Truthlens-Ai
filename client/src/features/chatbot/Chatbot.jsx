import { useEffect, useRef, useState } from 'react';
import {
  getChatHistory,
  sendChatMessage,
} from '../../services/api';

export default function Chatbot({ claimId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(true);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState('');
  const bottomRef = useRef(null);

  useEffect(() => {
    let active = true;

    async function loadHistory() {
      setLoading(true);
      setError('');

      try {
        const result = await getChatHistory(claimId);
        if (active) setMessages(result.messages || []);
      } catch (err) {
        if (active) {
          setError(err.message || 'Unable to load chat history.');
        }
      } finally {
        if (active) setLoading(false);
      }
    }

    loadHistory();

    return () => {
      active = false;
    };
  }, [claimId]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  async function handleSubmit(event) {
    event.preventDefault();

    const message = input.trim();
    if (!message || sending) return;

    setInput('');
    setError('');
    setSending(true);

   const tempId = `temp-${Date.now()}`;

setMessages((current) => [
  ...current,
  { id: tempId, role: 'user', content: message },
]);

try {
  const response = await sendChatMessage(claimId, message);

  setMessages((current) => [
    ...current.filter((item) => item.id !== tempId),
    { id: tempId, role: 'user', content: message },
    response,
  ]);
    } catch (err) {
      setError(err.message || 'Unable to send your message.');
    } finally {
      setSending(false);
    }
  }

  return (
    <section className="mt-6 rounded-2xl border border-white/10 bg-plum-surface p-5 sm:p-7">
      <h2 className="text-lg font-semibold">
        Evidence <span className="text-coral">Chat</span>
      </h2>

      <p className="mt-2 text-sm text-muted">
        Ask questions about this claim and its collected evidence.
      </p>

      <div className="mt-5 max-h-96 space-y-4 overflow-y-auto rounded-xl border border-white/10 bg-plum-background p-4">
        {loading ? (
          <p className="text-sm text-muted">Loading conversation...</p>
        ) : messages.length === 0 ? (
          <p className="text-sm text-muted">
            Try: “Which sources contradict this claim?”
          </p>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`max-w-[90%] rounded-xl p-3 ${
                message.role === 'user'
                  ? 'ml-auto bg-coral/15 text-cream'
                  : 'mr-auto bg-white/5 text-cream'
              }`}
            >
              <p className="mb-1 text-xs font-semibold text-lavender">
                {message.role === 'user' ? 'You' : 'TruthLens AI'}
              </p>
              <p className="whitespace-pre-wrap text-sm leading-6">
                {message.content}
              </p>
            </div>
          ))
        )}

        {sending && (
          <p className="text-sm text-muted">Analyzing evidence...</p>
        )}

        <div ref={bottomRef} />
      </div>

      {error && (
        <p role="alert" className="mt-3 text-sm text-red-300">
          {error}
        </p>
      )}

      <form onSubmit={handleSubmit} className="mt-4 flex gap-2">
        <input
          value={input}
          onChange={(event) => setInput(event.target.value)}
          maxLength={4000}
          placeholder="Ask about the evidence..."
          disabled={loading || sending}
          className="min-w-0 flex-1 rounded-xl border border-white/10 bg-plum-background px-4 py-3 text-sm outline-none focus:border-coral/60"
        />

        <button
          type="submit"
          disabled={loading || sending || !input.trim()}
          className="rounded-xl bg-coral px-4 py-3 text-sm font-semibold text-plum-background disabled:opacity-50"
        >
          {sending ? 'Sending...' : 'Send'}
        </button>
      </form>
    </section>
  );
}