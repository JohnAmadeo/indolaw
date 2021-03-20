import { Complex } from "utils/grammar";
import Law from "components/Law";
import React, { useState } from "react";
import TableOfContents from "components/TableOfContents";
import { darkColors, colors } from "utils/theme";
import Head from "next/head";
import { getDefaultSettings } from "http2";

// TODO(johnamadeo): Fix "Warning: Each child in a list should have a unique "key" prop." problem
export default function LawPage(props: {
  law: Complex;
}): JSX.Element {
  const border = "2px solid red";
  const navWidth = "400px";

  const [isDarkMode, setIsDarkMode] = useState(false);

  return (
    <div>
      <Head>
        <title>UU No. 11 Tahun 2020</title>
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      </Head>
      <div className="table-of-contents-container">
        <style jsx>{`
          .table-of-contents-container {
            height: 100%;
            overflow: auto;
            position: fixed;
            padding: 20px;
            width: ${navWidth};
            background-color: ${(isDarkMode ? darkColors : colors).trayBackground};
          }

          @media screen and (max-width: 768px) {
            .table-of-contents-container {
              top: 0;
              height: 60px;
              overflow: hidden;
              width: 100vw;
              z-index: 1;
            }
          }
        `}</style>
        <TableOfContents law={props.law} isDarkMode={isDarkMode} setIsDarkMode={() => setIsDarkMode(!isDarkMode)} />
      </div>

      <div className="law-container">
        <style jsx>{`
          .law-container {
            background-color: ${(isDarkMode ? darkColors : colors).background};
            position: absolute;
            left: ${navWidth};
            right: 0;
          }

          .law {
            margin: 0 auto;
            width: 768px;
          }

          @media screen and (max-width: 1224px) {
            .law {
              width: auto;
              padding: 0 24px;
            }
          }

          @media screen and (max-width: 768px) {
            .law-container {
              position: absolute;
              top: 60px;
              left: 0;
              overflow: scroll;
              height: calc(100% - 80px);
              font-size: 14px;
              // border: ${border};
            }
          }
        `}</style>
        <div className="law">
          <Law law={props.law} isDarkMode={isDarkMode}/>
        </div>
      </div>
    </div>
  );
}