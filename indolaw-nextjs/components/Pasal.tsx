import { CSSProperties, useState } from "react";
import { Complex, Primitive, renderStructure } from "utils/grammar";
import { useAppContext } from "utils/context-provider";
import PrimitiveStructure from "./PrimitiveStructure";
import { Structure } from "utils/grammar";
import ReactDOMServer from "react-dom/server";
import { useMediaQuery } from "react-responsive";
import * as clipboard from "clipboard-polyfill";
import CopyButton from "./CopyButton";
import { renderCopyPasalHtml } from "utils/copypaste";

export default function Pasal(props: {
  structure: Complex,
  numOfHeadingLines: number,
}): JSX.Element {
  const { structure, numOfHeadingLines } = props;
  const isMobile = useMediaQuery({ query: "(max-width: 768px)" });

  const { colorScheme } = useAppContext();

  const headingStyle: CSSProperties = {
    marginLeft: "0px",
    textAlign: "center",
    margin: "8px 0",
    fontWeight: 700,
  };

  const htmlToCopy = ReactDOMServer.renderToStaticMarkup(
    renderCopyPasalHtml(structure)
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

        console.log(htmlToCopy);
      }}
    />
  );

  const isModifiedPasal = structure.type === Structure.MODIFIED_PASAL;
  return (
    <>
      <style jsx>{`
        .container {
          margin: ${isModifiedPasal ? '0' : '48px'} 0 0 0;
          display: flex;
          justify-content: center;
        }
      `}</style>
      <div
        className="container"
        id={structure.id}
      >
        <PrimitiveStructure
          structure={structure.children[0] as Primitive}
          customStyle={headingStyle}
        />
        {!isMobile && copyButton}
      </div>
      {structure.children
        .slice(numOfHeadingLines)
        .map((child, idx) => renderStructure(child, idx))}
    </>
  );
}