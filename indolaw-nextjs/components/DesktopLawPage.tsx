import { LawData } from "utils/grammar";
import Law from "components/Law";
import { useState } from "react";
import Head from "next/head";
import { useAppContext } from "../utils/context-provider";
import Tray from "./Tray";

// TODO(johnamadeo): Fix "Warning: Each child in a list should have a unique "key" prop." problem
export default function DesktopLawPage(props: {
  law: LawData;
}): JSX.Element {
  const [isTrayExpanded, setIsTrayExpanded] = useState(true);
  const { colorScheme } = useAppContext();

  const expandedTrayWidth = 320;
  // Ideally we'd want to set the width of the minimized tray to just 'inherit' so that it'll be as
  // wide as its contents; however in order to animate the tray collapsing/expanding we cannot use
  // 'inherit' due to a CSS transition limitation. See https://css-tricks.com/using-css-transitions-auto-dimensions/
  const minimizedTrayWidth = 44;
  const trayWidth = isTrayExpanded ? expandedTrayWidth : minimizedTrayWidth;

  return (
    <div className="container">
      <style jsx>{`
        .container {
          display: flex;
          height: 100%;
        }

        .law-container {
          flex-grow: 1;
          max-width: calc(100% - ${trayWidth}px);
          transition: max-width ease 0.2s;
          background-color: ${colorScheme.background};
        }

        .law {
          margin: 24px auto 0 auto;
          width: 768px;
        }

        @media screen and (max-width: 1224px) {
          .law {
            width: auto;
            padding: 0 24px;
          }
        }
      `}</style>
      <Tray
        law={props.law}
        isExpanded={isTrayExpanded}
        onExpand={() => setIsTrayExpanded(true)}
        onMinimize={() => setIsTrayExpanded(false)}
        width={trayWidth}
      />

      <div className="law-container">

        <div className="law">
          <Law law={props.law.content} colorScheme={colorScheme} />
        </div>
      </div>
    </div>
  );
}