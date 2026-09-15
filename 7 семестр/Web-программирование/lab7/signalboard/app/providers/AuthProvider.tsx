// Синхронизирует клиентский интерфейс с серверной cookie-сессией.

"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";

export type UserDTO = {
  id: string;
  name: string;
  email: string;
};

type AuthStatus = "loading" | "authenticated" | "guest";

type AuthContextValue = {
  user: UserDTO | null;
  status: AuthStatus;
  refresh: () => Promise<void>;
  login: (email: string, password: string) => Promise<void>;
  register: (input: {
    name: string;
    email: string;
    password: string;
    confirmPassword: string;
  }) => Promise<void>;
  logout: () => Promise<void>;
};

const AuthContext = createContext<AuthContextValue | null>(null);

// Читаем безопасное сообщение из согласованного JSON-ответа.
async function readError(response: Response): Promise<string> {
  const payload = (await response.json().catch(() => null)) as
    | { error?: string; errors?: string[] }
    | null;

  return payload?.errors?.[0] ?? payload?.error ?? "Ошибка запроса";
}

export default function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserDTO | null>(null);
  const [status, setStatus] = useState<AuthStatus>("loading");

  // Восстанавливаем состояние из серверной cookie, не читая её на клиенте.
  const fetchCurrentUser = useCallback(async (): Promise<UserDTO | null> => {
    const response = await fetch("/api/auth/me", {
      cache: "no-store",
      credentials: "same-origin",
    });

    if (!response.ok) {
      return null;
    }

    const payload = (await response.json()) as { user: UserDTO | null };
    return payload.user;
  }, []);

  const refresh = useCallback(async () => {
    const currentUser = await fetchCurrentUser();

    setUser(currentUser);
    setStatus(currentUser ? "authenticated" : "guest");
  }, [fetchCurrentUser]);

  useEffect(() => {
    void fetchCurrentUser().then((currentUser) => {
      setUser(currentUser);
      setStatus(currentUser ? "authenticated" : "guest");
    });
  }, [fetchCurrentUser]);

  const login = useCallback(async (email: string, password: string) => {
    const response = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "same-origin",
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) throw new Error(await readError(response));

    const payload = (await response.json()) as { user: UserDTO };
    setUser(payload.user);
    setStatus("authenticated");
  }, []);

  const register = useCallback(async (input: {
    name: string;
    email: string;
    password: string;
    confirmPassword: string;
  }) => {
    const response = await fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "same-origin",
      body: JSON.stringify(input),
    });

    if (!response.ok) throw new Error(await readError(response));

    const payload = (await response.json()) as { user: UserDTO };
    setUser(payload.user);
    setStatus("authenticated");
  }, []);

  const logout = useCallback(async () => {
    const response = await fetch("/api/auth/logout", {
      method: "POST",
      credentials: "same-origin",
    });

    if (!response.ok) throw new Error(await readError(response));
    setUser(null);
    setStatus("guest");
  }, []);

  // Стабилизируем объект контекста для дочерних Client Components.
  const value = useMemo(
    () => ({ user, status, refresh, login, register, logout }),
    [user, status, refresh, login, register, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const value = useContext(AuthContext);
  if (!value) throw new Error("useAuth must be used inside AuthProvider");
  return value;
}
