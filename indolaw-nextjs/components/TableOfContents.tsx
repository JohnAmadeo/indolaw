import { useState } from "react";
import { Structure, Complex, Primitive } from "utils/grammar";
import Link from "next/link";
import { colors, fonts, TableOfContentsStyle } from "utils/theme";
import TableOfContentsGroup from "components/TableOfContentsGroup";
import { useMediaQuery } from "react-responsive";

export default function TableOfContents(props: { law: Complex }): JSX.Element {
  const isMobile = useMediaQuery({ query: "(max-width: 768px)" });

  const style: TableOfContentsStyle = {
    backgroundColor: isMobile ? "#1a6e94" : "transparent",
    iconSize: 22 * 1.2,
    fontSize: 22,
    iconTextGap: 22 / 4,
  };

  const tableOfContents = props.law.children.map((child) => (
    <TableOfContentsGroup structure={child} depth={0} isMobile={isMobile} />
  ));

  return (
    <div>
      {isMobile ? (
        <MobileTableOfContents
          law={props.law}
          isMobile={isMobile}
          style={style}
        />
      ) : (
        tableOfContents
      )}
    </div>
  );
}

function MobileTableOfContents(props: {
  law: Complex;
  isMobile: boolean;
  style: TableOfContentsStyle;
}): JSX.Element {
  const [isExpanded, setIsExpanded] = useState(true);

  // TODO(johnamadeo): TableOfContentsGroup needs to take in a onSelect callback
  // so we can minimize the ToC
  const tableOfContents = props.law.children.map((child) => (
    <TableOfContentsGroup
      structure={child}
      depth={0}
      isMobile={props.isMobile}
    />
  ));

  return isExpanded ? (
    <div>
      <style jsx>{`
        div {
          background-color: ${colors.background};
          position: fixed;
          top: 0;
          left: 0;
          width: 100vw;
          height: 100vh;
          border: 1px solid red;
          z-index: 1;
          padding: 20px;
          overflow: scroll;
        }
      `}</style>
      <button onClick={() => setIsExpanded(false)}>Go Back</button>
      {tableOfContents}
    </div>
  ) : (
    <button onClick={() => setIsExpanded(true)}>Daftar Isi</button>
  );
}
