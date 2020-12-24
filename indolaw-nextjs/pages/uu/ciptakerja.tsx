import fs from "fs";
import { GetStaticProps } from "next";
import { Complex } from "utils/grammar";
import Law from "components/Law";
import React from "react";
import TableOfContents from "components/TableOfContents";
import { colors } from "utils/theme";
import Head from "next/head";

// TODO(johnamadeo): Fix "Warning: Each child in a list should have a unique "key" prop." problem
export default function Test(props: {
  data: {
    law: Complex;
  };
}): JSX.Element {
  const border = "2px solid red";
  const navWidth = "400px";

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
            background-color: ${colors.background};
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
        <TableOfContents law={props.data.law} />
      </div>

      <div className="law-container">
        <style jsx>{`
          .law-container {
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
          <Law law={props.data.law} />
        </div>
      </div>
    </div>
  );
}

export const getStaticProps: GetStaticProps = async () => {
  const filePath = "../indolaw-parser/omnibus_law_pg_3_13_modified.json";
  const file = fs.readFileSync(filePath, "utf8");

  return {
    props: {
      data: {
        law: JSON.parse(file),
      },
    },
  };
};
