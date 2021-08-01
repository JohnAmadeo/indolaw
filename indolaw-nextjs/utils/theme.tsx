const commonTrayColors = {
  background: "#373d3f",
  text: "#f2f2f2",
  textSecondary: "#afb1b2",
};

export const colors = {
  background: "#ffffff",
  backgroundSecondary: '#f5f5f5',
  text: "#372b25",
  textHover: '#8b8b8b',
  clickable: '#a79565',
  clickableBackground: 'rgb(167, 149, 101, 0.1)',
  linkText: "#373d3f",
  subcontent: {
    background: "#eaeaea"
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
  backgroundSecondary: '#242424',
  text: "#ffffff",
  textHover: "#afafaf",
  clickable: '#a79565',
  clickableBackground: 'rgb(167, 149, 101, 0.1)',
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
  background: '',
  backgroundSecondary: '',
  text: '',
  textHover: '',
  clickable: '',
  clickableBackground: '',
  linkText: '',
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
  background: string,
  backgroundSecondary: string,
  text: string,
  textHover: string,
  clickable: string,
  clickableBackground: string,
  linkText: string,
  subcontent: {
    background: string,
  },
  tray: {
    button: string;
    buttonHover: string;
    buttonText: string;
    background: string;
    text: string;
    textSecondary: string;
  };
}
