# Frontend — AI Chatbot Enterprise

React + Vite + TypeScript. Chat Console + Login + Citations panel.

## Run (Docker from root)

```bash
make dev-up
```

UI: http://localhost:5173

## Run locally (without Docker)

```bash
cd frontend
npm install
npm run dev
```

Configure the API via `VITE_API_BASE_URL` (defaults to `http://localhost:8000`).

## Structure

```
src/
  api/client.ts          typed API client (auth, chat) + token
  components/
    Login.tsx            sign in / sign up
    ChatConsole.tsx      main chat shell
    Citations.tsx        display citations (required for RAG)
  App.tsx
```

> Hold-to-Talk (voice) will be added in Phase 4–5 once the voice backend is ready.
