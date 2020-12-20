import { useState } from "react";
import { Complex } from "utils/grammar";
import { colors, fonts } from "utils/theme";
import TableOfContentsGroup from "components/TableOfContentsGroup";
import { useMediaQuery } from "react-responsive";

export default function TableOfContents(props: { law: Complex }): JSX.Element {
  const isMobile = useMediaQuery({ query: "(max-width: 768px)" });
  const [isExpanded, setIsExpanded] = useState(false);

  const tableOfContents = props.law.children.map((child) => (
    <TableOfContentsGroup
      structure={child}
      depth={0}
      isMobile={isMobile}
      onSelectLink={() => {
        if (isMobile) {
          setIsExpanded(false);
        }
      }}
    />
  ));

  if (!isMobile) {
    return <>{tableOfContents}</>;
  }

  return isExpanded ? (
    <div className="container">
      <style jsx>{`
        .container {
          background-color: ${colors.background};
          position: fixed;
          top: 0;
          left: 0;
          width: 100vw;
          height: 100vh;
          // border: 1px solid red;
          z-index: 1;
          padding: 20px;
          overflow: scroll;
        }

        .back {
          margin-bottom: 12px;
          height: 40px;
          border-bottom: 1px solid ${colors.dark.text};
        }

        .table-of-contents {
          padding: 4px 0px;
          position: absolute;
          top: 60px;
          height: calc(100% - 60px);
          left: 20px;
          right: 20px;
          overflow: scroll;
        }

        span {
          color: ${colors.dark.text};
          font-family: ${fonts.sans};
          font-size: 18px;
        }

        .material-icons.style {
          vertical-align: bottom;
        }
      `}</style>
      <div className="back">
        <span onClick={() => setIsExpanded(false)}>
          <i className="material-icons style">chevron_left</i>Kembali
        </span>
      </div>
      <div className="table-of-contents">{tableOfContents}</div>
    </div>
  ) : (
    <>
      <style jsx>{`
        span {
          text-align: center;
          font-size: 18px;
          font-family: ${fonts.sans};
          color: ${colors.dark.text};
        }

        .material-icons.style {
          vertical-align: bottom;
        }
      `}</style>
      <span
        onClick={() => {
          setIsExpanded(true);
        }}
      >
        <i className="material-icons style">expand_more</i> Daftar Isi
      </span>
    </>
  );
}
