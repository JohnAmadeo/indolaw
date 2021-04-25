import { AppContextWrapper } from "utils/context-provider";
import { AppProps } from 'next/app';
import "../styles/globals.css";

function MyApp({ Component, pageProps }: AppProps) {
  return (
    <AppContextWrapper>
      <Component {...pageProps} />
    </AppContextWrapper>
  );
}

export default MyApp;
