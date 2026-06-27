const API_BASE = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

const TOKEN_KEY = "ai_chat_token";

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

async function request<T>(path: string, options: RequestInit = {}): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };
  const token = getToken();
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const resp = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (resp.status === 401 || resp.status === 403) {
    clearToken();
    throw new Error("Phiên đăng nhập không hợp lệ. Vui lòng đăng nhập lại.");
  }
  if (!resp.ok) {
    const detail = await resp.json().catch(() => ({}));
    throw new Error(detail.detail ?? `Lỗi ${resp.status}`);
  }
  return resp.json() as Promise<T>;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  role: string;
}

export interface Citation {
  type: string;
  doc_id: string;
  version?: string | null;
  source?: string | null;
  page?: number | null;
  sheet?: string | null;
  cell_range?: string | null;
  snippet?: string | null;
}

export interface ChatResponse {
  conversation_id: string;
  answer: string;
  citations: Citation[];
}

export const api = {
  register: (email: string, password: string, role = "ENGINEER") =>
    request<TokenResponse>("/api/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password, role }),
    }),
  login: (email: string, password: string) =>
    request<TokenResponse>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  chat: (message: string, conversationId?: string) =>
    request<ChatResponse>("/api/chat", {
      method: "POST",
      body: JSON.stringify({ message, conversation_id: conversationId }),
    }),
};
