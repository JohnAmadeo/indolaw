import { LawData } from "utils/grammar";
import Law from "components/Law";
import React from "react";
import MobileTray from "components/MobileTray";
import { useAppContext } from "../utils/context-provider";

// TODO(johnamadeo): Fix "Warning: Each child in a list should have a unique "key" prop." problem
export default function MobileLawPage(props: {
  law: LawData;
}): JSX.Element {
  const { colorScheme } = useAppContext();

  // TODO: Add the PDF links
  if (props.law.content == null) {
    return <></>;
  }

  return (
    <div>
      <div className="law-container">
        <style jsx>{`
          .law {
            width: auto;
            padding: 0 24px;
          }

          .law-container {
            background-color: ${colorScheme.background};
            position: absolute;
            left: 0;
            overflow: scroll;
            height: 100%;
            font-size: 14px;
          }
        `}</style>
        <div className="law">
          <Law law={props.law.content} metadata={props.law.metadata} colorScheme={colorScheme} />
        </div>
      </div>
    </div>
  );
}