const commonTrayColors = {
  background: "#373d3f",
  text: "#f2f2f2",
  textSecondary: "#afb1b2",
};

export const colors = {
  background: "#ffffff",
  backgroundSecondary: '#f5f5f5',
  text: "#514d48",
  textHover: '#818181',
  linkText: "#373d3f",
  tray: {
    button: '#1b1c1d',
    buttonHover: '#2a2f31',
    buttonText: '#ffffff',
    ...commonTrayColors
  },
};

export const darkColors = {
  background: "#1b1c1d",
  backgroundSecondary: '#242424',
  text: "#ffffff",
  textHover: '#dadada',
  linkText: '#1ecbe1',
  tray: {
    button: '#ffffff',
    buttonHover: '#bbbbbb',
    buttonText: '#514d48',
    ...commonTrayColors
  },
};

export const noColors = {
  background: '',
  backgroundSecondary: '',
  text: '',
  textHover: '',
  linkText: '',
  tray: {
    button: '',
    buttonHover: '',
    buttonText: '',
    background: '',
    text: '',
    textSecondary: '',
  }
}

export const fonts = {
  sans: "Merriweather Sans",
  serif: "Merriweather",
};

export interface ColorScheme {
  background: string,
  backgroundSecondary: string,
  text: string,
  textHover: string,
  linkText: string,
  tray: {
    button: string,
    buttonHover: string,
    buttonText: string,
    background: string,
    text: string,
    textSecondary: string,
  }
}