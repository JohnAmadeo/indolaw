const commonTrayColors = {
  background: "#373d3f",
  text: "#f2f2f2",
  textSecondary: "#afb1b2",
};

export const colors = {
  background: "#ffffff",
  text: "#514d48",
  textHover: '#818181',
  linkText: "#373d3f",
  subcontent: { 
    background: "#d3d3d3" 
  },
  tray: {
    button: "#1b1c1d",
    buttonHover: "#2a2f31",
    buttonText: "#ffffff",
    ...commonTrayColors,
  },
};

export const darkColors = {
  background: "#1b1c1d",
  text: "#ffffff",
  textHover: "#dadada",
  linkText: "#1ecbe1",
  subcontent: { 
    background: "#373d3f" 
  },
  tray: {
    button: "#ffffff",
    buttonHover: "#bbbbbb",
    buttonText: "#514d48",
    ...commonTrayColors,
  },
};

export const noColors = {
  background: "",
  text: "",
  linkText: "",
  subcontent: {
    background: "",
  },
  tray: {
    button: "",
    buttonHover: "",
    buttonText: "",
    background: "",
    text: "",
    textSecondary: "",
  },
};

export const fonts = {
  sans: "Merriweather Sans",
  serif: "Merriweather",
};

export interface ColorScheme {
  background: string;
  text: string;
  textHover: string;
  linkText: string;
  subcontent: {
    background: string;
  };
  tray: {
    button: string;
    buttonHover: string;
    buttonText: string;
    background: string;
    text: string;
    textSecondary: string;
  };
}
