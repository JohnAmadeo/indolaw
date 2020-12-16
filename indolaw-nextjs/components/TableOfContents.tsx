import { useState } from "react";
import { Structure, Complex, Primitive } from "utils/grammar";
import Link from "next/link";
import { colors, fonts } from "utils/theme";
import ExpandLess from "assets/ExpandLess.svg";
import ExpandMore from "assets/ExpandMore.svg";
import TableOfContentsGroup from "components/TableOfContentsGroup";
import { useMediaQuery } from "react-responsive";

export default function TableOfContents(props: { law: Complex }): JSX.Element {
  const isMobile = useMediaQuery({ query: "(max-width: 768px)" });

  const tableOfContents = props.law.children.map((child) => (
    <TableOfContentsGroup structure={child} depth={0} />
  ));

  return (
    <div>
      {isMobile ? <MobileTableOfContents law={props.law} /> : tableOfContents}
    </div>
  );
}

function MobileTableOfContents(props: { law: Complex }): JSX.Element {
  const [isExpanded, setIsExpanded] = useState(false);

  const tableOfContents = props.law.children.map((child) => (
    <TableOfContentsGroup structure={child} depth={0} />
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
        }
      `}</style>
      <button onClick={() => setIsExpanded(false)}>Go Back</button>
      {tableOfContents}
    </div>
  ) : (
    <button onClick={() => setIsExpanded(true)}>
      Daftar Isi <ExpandMore />
    </button>
  );
}
