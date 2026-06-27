# Frontend — AI Chatbot Enterprise

React + Vite + TypeScript. Chat Console + Login + Citations panel.

## Chạy (Docker từ root)

```bash
make dev-up
```

UI: http://localhost:5173

## Chạy local (không Docker)

```bash
cd frontend
npm install
npm run dev
```

Cấu hình API qua `VITE_API_BASE_URL` (mặc định `http://localhost:8000`).

## Cấu trúc

```
src/
  api/client.ts          typed API client (auth, chat) + token
  components/
    Login.tsx            đăng nhập / đăng ký
    ChatConsole.tsx      khung chat chính
    Citations.tsx        hiển thị trích dẫn (bắt buộc cho RAG)
  App.tsx
```

> Hold-to-Talk (voice) sẽ được thêm ở Phase 4–5 sau khi voice backend sẵn sàng.
