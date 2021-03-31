import { createContext, useContext, useState } from 'react';

const AppContext = createContext();

export function ContextWrapper({ children }) {
    const [darkTheme, setDarkTheme] = useState(false);

    let state = {
        darkTheme,
        setDarkTheme
    }

    return (
        <AppContext.Provider value={state}>
        {children}
        </AppContext.Provider>
    );
}

export function useAppContext() {
  return useContext(AppContext);
}
