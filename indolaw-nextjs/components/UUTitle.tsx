import { CSSProperties, useState } from "react";
import { Complex, Primitive } from "utils/grammar";
import { useAppContext } from "utils/context-provider";
import PrimitiveStructure from "./PrimitiveStructure";
import { useMediaQuery } from "react-responsive";
import * as clipboard from "clipboard-polyfill";
import CopyButton from "./CopyButton";

export default function UUTitle(props: {
  structure: Complex,
}): JSX.Element {
  const { structure } = props;
  const [isHoverOnCopyButton, setIsHoverOnCopyButton] = useState(false);
  const { colorScheme } = useAppContext();
  const isMobile = useMediaQuery({ query: "(max-width: 768px)" });

  const headingStyle: CSSProperties = {
    marginLeft: "0px",
    textAlign: "center",
    margin: "8px 0",
    fontWeight: 700,
  };

  const uuTitle = structure.children.reduce(
    (sentence, child) => {
      return `${sentence} ${(child as Primitive).text}`;
    },
    '',
  );

  const copyButton = (
    <CopyButton
      onClick={async () => await clipboard.writeText(uuTitle)}
      onMouseEnter={() => setIsHoverOnCopyButton(true)}
      onMouseLeave={() => setIsHoverOnCopyButton(false)}
    />
  );

  return (
    <>
      <style jsx>{`
        .container {
          margin: 12px 0;
          padding: 12px 0;
          box-sizing: border-box;
          background-color: ${isHoverOnCopyButton ? colorScheme.backgroundSecondary : 'none'};
          border-radius: 8px;
        }

        .copy-button-and-text-container {
          margin-bottom: -4px;
          display: flex;
          justify-content: center;
        }

      `}</style>
      <div id={structure.id} className="container">
        {structure.children.map((child, idx) => {
          if (idx === 0) {
            return (
              <div className="copy-button-and-text-container">
                <PrimitiveStructure
                  key={idx}
                  structure={child as Primitive}
                  customStyle={headingStyle}
                />
                {!isMobile && copyButton}
              </div>
            );
          }

          return (
            <PrimitiveStructure
              key={idx}
              structure={child as Primitive}
              customStyle={headingStyle}
            />
          );
        })}
      </div>
    </>
  );
}
