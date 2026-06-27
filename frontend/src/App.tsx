import { useState } from "react";
import { ChatConsole } from "./components/ChatConsole";
import { Login } from "./components/Login";
import { getToken } from "./api/client";

export default function App() {
  const [authed, setAuthed] = useState<boolean>(() => !!getToken());
  const [role, setRole] = useState<string>("VIEWER");

  if (!authed) {
    return (
      <Login
        onLoggedIn={(r) => {
          setRole(r);
          setAuthed(true);
        }}
      />
    );
  }

  return <ChatConsole role={role} onLogout={() => setAuthed(false)} />;
}
