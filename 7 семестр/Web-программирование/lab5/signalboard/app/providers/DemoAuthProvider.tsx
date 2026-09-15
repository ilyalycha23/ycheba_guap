// Хранит учебное состояние пользователя и предоставляет вход и выход через React Context.

"use client";

import {
  createContext,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from "react";

// Описываем данные учебного пользователя.
export type DemoUser = {
  name: string;
  email: string;
};

// Задаём контракт данных и функций контекста.
type DemoAuthContextValue = {
  user: DemoUser | null;
  login: (email: string) => void;
  register: (name: string, email: string) => void;
  logout: () => void;
};

const DemoAuthContext = createContext<DemoAuthContextValue | null>(null);

// Объявляем основной компонент этого файла.
export default function DemoAuthProvider({
  children,
}: Readonly<{ children: ReactNode }>) {
  // Создаём локальное состояние компонента.
  const [user, setUser] = useState<DemoUser | null>(null);

  // Мемоизируем объект контекста до изменения его зависимостей.
  const value = useMemo<DemoAuthContextValue>(
    () => ({
      user,
      login(email) {
        const name = email.split("@")[0]?.trim() || "Сосед";
        setUser({ name, email });
      },
      register(name, email) {
        setUser({ name: name.trim(), email });
      },
      logout() {
        setUser(null);
      },
    }),
    [user],
  );

  // Возвращаем JSX-разметку, которую React выведет на странице.
  return (
    <DemoAuthContext.Provider value={value}>
      {children}
    </DemoAuthContext.Provider>
  );
}

// Возвращаем контекст и защищаем хук от вызова вне провайдера.
export function useDemoAuth(): DemoAuthContextValue {
  const context = useContext(DemoAuthContext);

  if (!context) {
    throw new Error("useDemoAuth должен использоваться внутри DemoAuthProvider");
  }

  return context;
}
