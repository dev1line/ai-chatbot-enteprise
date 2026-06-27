import { useState } from "react";
import { api, setToken } from "../api/client";

export function Login({ onLoggedIn }: { onLoggedIn: (role: string) => void }) {
  const [email, setEmail] = useState("engineer@example.com");
  const [password, setPassword] = useState("demo123");
  const [mode, setMode] = useState<"login" | "register">("login");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      const resp =
        mode === "login"
          ? await api.login(email, password)
          : await api.register(email, password);
      setToken(resp.access_token);
      onLoggedIn(resp.role);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="login">
      <h1>AI Chatbot Enterprise</h1>
      <p className="subtitle">Actionable RAG · Multimodal Search</p>
      <form onSubmit={submit}>
        <label>
          Email
          <input value={email} onChange={(e) => setEmail(e.target.value)} type="email" required />
        </label>
        <label>
          Password
          <input
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            type="password"
            required
          />
        </label>
        {error && <div className="error">{error}</div>}
        <button type="submit" disabled={loading}>
          {loading ? "Processing..." : mode === "login" ? "Sign in" : "Sign up"}
        </button>
      </form>
      <button
        className="link"
        onClick={() => setMode(mode === "login" ? "register" : "login")}
      >
        {mode === "login" ? "Don't have an account? Sign up" : "Already have an account? Sign in"}
      </button>
    </div>
  );
}
