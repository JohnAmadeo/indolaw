import { createContext, useContext, useState } from "react";
import { colors, darkColors } from "utils/theme";

const AppContext = createContext();

export function ContextWrapper({ children }) {
  const [darkTheme, setDarkTheme] = useState(false);
  const [tooltip, setTooltip] = useState({
    content: "",
    xPosition: 0,
    yPosition: 0
  });

  const toggleDarkMode = () => setDarkTheme(!darkTheme);
  const colorScheme = darkTheme ? darkColors : colors;
  const invertedColorScheme = darkTheme ? colors : darkColors;

  let state = {
    colorScheme,
    invertedColorScheme,
    toggleDarkMode,
    tooltip,
    setTooltip,
  };

  return <AppContext.Provider value={state}>{children}</AppContext.Provider>;
}

export function useAppContext() {
  return useContext(AppContext);
}
