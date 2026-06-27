import { useState } from "react";
import { api, clearToken, type Citation } from "../api/client";
import { Citations } from "./Citations";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  citations?: Citation[];
}

export function ChatConsole({ role, onLogout }: { role: string; onLogout: () => void }) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function send(e: React.FormEvent) {
    e.preventDefault();
    const text = input.trim();
    if (!text) return;
    setInput("");
    setError(null);
    setMessages((m) => [...m, { role: "user", content: text }]);
    setLoading(true);
    try {
      const resp = await api.chat(text, conversationId);
      setConversationId(resp.conversation_id);
      setMessages((m) => [
        ...m,
        { role: "assistant", content: resp.answer, citations: resp.citations },
      ]);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  function logout() {
    clearToken();
    onLogout();
  }

  return (
    <div className="chat">
      <header className="chat-header">
        <div>
          <strong>AI Chatbot Enterprise</strong>
          <span className="role-badge">{role}</span>
        </div>
        <button className="link" onClick={logout}>
          Đăng xuất
        </button>
      </header>

      <div className="messages">
        {messages.length === 0 && (
          <div className="empty">Hãy đặt câu hỏi về tài liệu đã release...</div>
        )}
        {messages.map((m, i) => (
          <div key={i} className={`msg msg-${m.role}`}>
            <div className="bubble">{m.content}</div>
            {m.role === "assistant" && m.citations && <Citations citations={m.citations} />}
          </div>
        ))}
        {loading && <div className="msg msg-assistant"><div className="bubble">Đang trả lời…</div></div>}
      </div>

      {error && <div className="error chat-error">{error}</div>}

      <form className="composer" onSubmit={send}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Nhập câu hỏi…"
          disabled={loading}
        />
        <button type="submit" disabled={loading || !input.trim()}>
          Gửi
        </button>
      </form>
    </div>
  );
}
