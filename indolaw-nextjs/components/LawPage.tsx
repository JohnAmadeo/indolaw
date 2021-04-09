import { LawData } from "utils/grammar";
import Law from "components/Law";
import React from "react";
import MobileTray from "components/MobileTray";
import Head from "next/head";
import { useAppContext } from "../utils/state-management/context-provider";
import { useMediaQuery } from "react-responsive";
import Tray from "./Tray";

// TODO(johnamadeo): Fix "Warning: Each child in a list should have a unique "key" prop." problem
export default function LawPage(props: {
  law: LawData;
}): JSX.Element {
  const border = "2px solid red";
  const navWidth = "400px";

  const isMobile = useMediaQuery({ query: "(max-width: 768px)" });
  const { colorScheme } = useAppContext();

  return (
    <div>
      <Head>
        <title>UU No. {props.law.metadata.number} Tahun {props.law.metadata.year}</title>
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
            background-color: ${colorScheme.tray.background};
          }

          @media screen and (max-width: 768px) {
            .table-of-contents-container {
              background-color: ${colorScheme.tray.background};
              top: 0;
              height: 60px;
              overflow: hidden;
              width: 100vw;
              z-index: 1;
            }
          }
        `}</style>
        {isMobile ? <MobileTray law={props.law} /> : <Tray law={props.law} />}
      </div>

      <div className="law-container">
        <style jsx>{`
          .law-container {
            background-color: ${colorScheme.background};
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
          <Law law={props.law.content} colorScheme={colorScheme} />
        </div>
      </div>
    </div>
  );
}