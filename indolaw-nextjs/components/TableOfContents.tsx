import { useState } from "react";
import { LawData } from "utils/grammar";
import { colors, fonts } from "utils/theme";
import TableOfContentsGroup from "components/TableOfContentsGroup";
import { useMediaQuery } from "react-responsive";
import { useAppContext } from "utils/state-management/context-provider";
import Citation from "./Citation";
import Divider from "./Divider";

export default function TableOfContents(props: { law: LawData }): JSX.Element {
  const isMobile = useMediaQuery({ query: "(max-width: 768px)" });
  const [isExpanded, setIsExpanded] = useState(false);
  const { colorScheme, invertedColorScheme, toggleDarkMode } = useAppContext();

  const tableOfContents = props.law.content.children.map((child, idx) => (
    <TableOfContentsGroup
      key={idx}
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

  const darkModeButton = (
    <>
      <style>{`
        button {
          cursor: pointer;
          height: 36px;
          padding: 4px 24px;
          background-color: ${invertedColorScheme.trayBackground};
          border-radius: 8px;
          border: 0;
          color: ${invertedColorScheme.tray.text};
          font-family: ${fonts.sans};
          font-size: 14px;
          ${isMobile ? "float: right; margin-top: -8px;" : "margin-bottom:16px"}
        }
      }`}</style>
      <button onClick={toggleDarkMode}>
        {colorScheme == colors ? "Dark Mode" : "Light Mode"}
      </button>
    </>
  );

  if (!isMobile) {
    return (
      <>
        {darkModeButton}
        <Citation metadata={props.law.metadata} />
        <Divider />
        {tableOfContents}
      </>
    );
  }

  return isExpanded ? (
    <div className="container">
      <style jsx>{`
        .container {
          background-color: ${colorScheme.trayBackground};
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
          border-bottom: 1px solid ${colorScheme.tray.text};
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
          color: ${colorScheme.tray.text};
          cursor: pointer;
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
        {darkModeButton}
      </div>
      <div className="table-of-contents">{tableOfContents}</div>
    </div>
  ) : (
    <>
      <style jsx>{`
        span {
          cursor: pointer;
          text-align: center;
          font-size: 18px;
          font-family: ${fonts.sans};
          color: ${colorScheme.tray.text};
        }

        .material-icons.style {
          vertical-align: bottom;
        }
      `}</style>
      <span onClick={() => {
        setIsExpanded(true);
      }}>
        <i className="material-icons style">expand_more</i> Daftar Isi
      </span>
      {darkModeButton}
    </>
  );
}
