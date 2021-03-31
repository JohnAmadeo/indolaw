import Document, { Html, Head, Main, NextScript } from "next/document";
import { ContextWrapper } from "../utils/state-management/context-provider";

class MyDocument extends Document {
  static async getInitialProps(ctx) {
    const initialProps = await Document.getInitialProps(ctx);
    return { ...initialProps };
  }

  render() {
    return (
      <Html>
        <Head>
          <link
            rel="stylesheet"
            href="https://fonts.googleapis.com/css?family=Merriweather|Merriweather+Sans"
          />
          <link
            href="https://fonts.googleapis.com/icon?family=Material+Icons"
            rel="stylesheet"
          ></link>
        </Head>
        <body>
            <Main />
            <NextScript />
        </body>
      </Html>
    );
  }
}

export default MyDocument;
