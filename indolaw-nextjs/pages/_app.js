import { ContextWrapper } from "utils/state-management/context-provider";
import "../styles/globals.css";

function MyApp({ Component, pageProps }) {
  return <ContextWrapper>
    <Component {...pageProps} />
    </ContextWrapper>;
}

export default MyApp;
