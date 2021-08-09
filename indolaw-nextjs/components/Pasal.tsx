import { CSSProperties, MutableRefObject, useContext, useEffect, useRef, useState } from "react";
import { Complex, Primitive, renderStructure } from "utils/grammar";
import PrimitiveStructure from "./PrimitiveStructure";
import { renderPenjelasan } from "utils/grammar";
import ReactDOMServer from "react-dom/server";
import * as clipboard from "clipboard-polyfill";
import CopyButton from "./CopyButton";
import { renderCopyHtml } from "utils/copypaste";
import { LawContext, getPenjelasanMapKey, VisibilityContext } from "utils/context-provider";
import { useAppContext } from "utils/context-provider";
import { useIsMobile } from "utils/hooks";

export default function Pasal(props: {
  structure: Complex,
  numOfHeadingLines: number,
}): JSX.Element {
  const { structure, numOfHeadingLines } = props;
  const isMobile = useIsMobile();
  const { penjelasanMap } = useContext(LawContext);
  const [isHoverOnCopyButton, setIsHoverOnCopyButton] = useState(false);
  const { colorScheme } = useAppContext();
  const pasalRef: MutableRefObject<HTMLDivElement | null> = useRef(null);

  const { setElement, setIsVisible } = useContext(VisibilityContext);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries, _) => {
        if (entries.length !== 1) {
          return;
        }

        if (setIsVisible != null) {
          setIsVisible(structure.id, entries[0].isIntersecting);
        }
      },
      {
        threshold: 0.25,
      }
    )

    if (pasalRef.current != null && setElement != null) {
      observer.observe(pasalRef.current);
      setElement(structure.id, pasalRef.current);
    }

    return () => {
      observer.disconnect();
    }
  }, [pasalRef, setElement, setIsVisible]);


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
      onMouseEnter={() => setIsHoverOnCopyButton(true)}
      onMouseLeave={() => setIsHoverOnCopyButton(false)}
    />
  );

  const isPerubahanStructure = structure.type.includes('PERUBAHAN');
  const isPenjelasanStructure = structure.type.includes('PENJELASAN');
  // Collapse penjelasan on default if it's a parent penjelasan node (comes from a Pasal mapping),
  // otherwise, it shouldn't be collapsed (ex: if it's a penjelasan_pasal_perubahan as a part of penjelasan_pasal) 
  const collapsePenjelasanOnDefault = !isPenjelasanStructure;

  const pasalNumber = structure.children[0] as Primitive;
  const key = getPenjelasanMapKey(structure.type, pasalNumber.text);
  const penjelasanPasal = penjelasanMap[key];

  return (
    <div className="container" ref={pasalRef} id={structure.id}>
      <style jsx>{`
        .container {
          margin: ${isPerubahanStructure ? "0" : "48px"} 0 0 0;
          background-color: ${isHoverOnCopyButton ? colorScheme.clickableBackground : 'none'};
          border-radius: 8px;
          padding: 4px 24px;
        }

        .pasal-number {
          display: flex;
          justify-content: center;
        }
      `}</style>
      <div className="pasal-number">
        <PrimitiveStructure
          structure={pasalNumber}
          customStyle={headingStyle}
        />
        {!isMobile && copyButton}
      </div>
      {structure.children
        .slice(numOfHeadingLines)
        .map((child, idx) => renderStructure(child, idx, isMobile))}
      {!isPenjelasanStructure &&
        penjelasanPasal != null &&
        renderPenjelasan(
          penjelasanPasal,
          undefined,
          collapsePenjelasanOnDefault
        )}
    </div>
  );
}