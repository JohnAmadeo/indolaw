import Document, { Html, Head, Main, NextScript } from "next/document";

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
            rel="preload"
            href="/fonts/Merriweather/Merriweather-Regular.ttf"
            as="font"
            crossOrigin=""
          ></link>
          <link 
            rel="preload"
            href="/fonts/Merriweather/Merriweather-Italic.ttf"
            as="font"
            crossOrigin=""
          ></link>
          <link 
            rel="preload"
            href="/fonts/Merriweather/Merriweather-Bold.ttf"
            as="font"
            crossOrigin=""
          ></link>
          <link 
            rel="preload"
            href="/fonts/Merriweather/MerriweatherSans-Regular.ttf"
            as="font"
            crossOrigin=""
          ></link>
          <link 
            rel="preload"
            href="/fonts/Merriweather/MerriweatherSans-Italic.ttf"
            as="font"
            crossOrigin=""
          ></link>
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
