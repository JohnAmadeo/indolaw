import { CSSProperties, useState } from "react";
import { Complex, Primitive, renderStructure } from "utils/grammar";
import { useAppContext } from "../utils/context-provider";
import PrimitiveStructure from "./PrimitiveStructure";
import ReactDOMServer from "react-dom/server";
import * as clipboard from "clipboard-polyfill";
import CopyButton from "./CopyButton";
import { renderCopyHtml } from "utils/copypaste";
import { useMediaQuery } from "react-responsive";

export default function PenjelasanPasal(props: {
  structure: Complex;
  numOfHeadingLines: number;
}): JSX.Element {
  const { structure, numOfHeadingLines } = props;
  const [isContentVisible, setIsContentVisible] = useState(false);
  const { colorScheme } = useAppContext();
  const isMobile = useMediaQuery({ query: "(max-width: 768px)" });

  const headingStyle: CSSProperties = {
    marginLeft: "0px",
    textAlign: "center",
    margin: "8px 0",
    fontWeight: 700,
  };

  const htmlToCopy = ReactDOMServer.renderToStaticMarkup(
    renderCopyHtml(structure)
  );

  const copyButton = (
    <CopyButton
      onClick={async () => {
        const item = new clipboard.ClipboardItem({
          "text/html": new Blob(
            [htmlToCopy],
            { type: "text/html" }
          )
        });
        await clipboard.write([item]);
      }}
    />
  );

  return (
    <>
      <style jsx>{`
        .group {
          margin: 20px auto;
          background-color: ${colorScheme.subcontent.background};
          padding: 10px 20px;
          border-radius: 7.5px;
        }

        .title:hover {
          cursor: pointer;
        }

        .title {
          margin: 8px 0;
          font-weight: 700;
          line-height: 1.5;
          display: flex;
          justify-content: center;
        }

        .content {
          margin-top: 20px;
        }

        .heading-container {
          display: flex;
          justify-content: center;
        }

        .material-icons.style {
          vertical-align: bottom;
          padding-top: 2px;
        }
      `}</style>
      <div className="group">
        <div
          className="title"
          onClick={() => setIsContentVisible(!isContentVisible)}
        >
          Penjelasan
          <i className="material-icons style">
            {isContentVisible ? "expand_less" : "expand_more"}
          </i>
        </div>

        {isContentVisible && (
          <div className="content">
            <div id={structure.id} className="heading-container">
              <PrimitiveStructure
                structure={structure.children[0] as Primitive}
                customStyle={headingStyle}
              />
              {!isMobile && copyButton}
            </div>

            {structure.children.slice(numOfHeadingLines).map((child, idx) => {
              child = child as Primitive;
              // The if-statement below should be temporary, as the current parser parses "TAMBAHAN xxxx" as part of penjelasan
              // which should not be the intended behavior
              if (
                child.text &&
                child.text.startsWith(
                  "TAMBAHAN LEMBARAN NEGARA REPUBLIK INDONESIA"
                )
              ) {
                return <></>;
              }

              return renderStructure(child, idx);
            })}
          </div>
        )}
      </div>
    </>
  );
}
