import { createContext, useContext, useState } from 'react';
import { colors, darkColors } from 'utils/theme';

const AppContext = createContext();

export function ContextWrapper({ children }) {
    const [darkTheme, setDarkTheme] = useState(false);

    const toggleDarkMode = () => setDarkTheme(!darkTheme);
    const colorScheme = darkTheme ? darkColors : colors;
    const invertedColorScheme = darkTheme ? colors : darkColors;

    let state = {
        colorScheme,
        invertedColorScheme,
        toggleDarkMode
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
