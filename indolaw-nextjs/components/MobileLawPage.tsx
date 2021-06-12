import { LawData } from "utils/grammar";
import Law from "components/Law";
import React from "react";
import MobileTray from "components/MobileTray";
import Head from "next/head";
import { useAppContext } from "../utils/context-provider";
import { useMediaQuery } from "react-responsive";
import Tray from "./Tray";

// TODO(johnamadeo): Fix "Warning: Each child in a list should have a unique "key" prop." problem
export default function MobileLawPage(props: {
  law: LawData;
}): JSX.Element {
  const border = "2px solid red";
  const navWidth = "400px";

  const { colorScheme } = useAppContext();

  const tray = (
    <div className="table-of-contents-container">
      <style jsx>{`
        .table-of-contents-container {
          height: 100%;
          position: fixed;
          padding: 20px;
          background-color: ${colorScheme.tray.background};
          top: 0;
          height: 60px;
          overflow: hidden;
          width: 100vw;
          z-index: 1;
        }
      `}</style>
      <MobileTray law={props.law} />
    </div>
  );

  return (
    <div>
      {tray}

      <div className="law-container">
        <style jsx>{`
          .law {
            width: auto;
            padding: 0 24px;
          }

          .law-container {
            background-color: ${colorScheme.background};
            position: absolute;
            top: 60px;
            left: 0;
            overflow: scroll;
            height: calc(100% - 80px);
            font-size: 14px;
          }
        `}</style>
        <div className="law">
          <Law law={props.law.content} colorScheme={colorScheme} />
        </div>
      </div>
    </div>
  );
}