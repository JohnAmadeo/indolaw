import { useState } from "react";
import { LawData } from "utils/grammar";
import { colors, fonts } from "utils/theme";
import TableOfContentsGroup from "components/TableOfContentsGroup";
import { useAppContext } from "utils/context-provider";
import TrayButton from "./TrayButton";

export default function MobileTray(props: { law: LawData }): JSX.Element {
  const [isExpanded, setIsExpanded] = useState(false);
  const { colorScheme, invertedColorScheme, toggleDarkMode } = useAppContext();

  const tableOfContents = props.law.content.children.map((child, idx) => (
    <TableOfContentsGroup
      key={idx}
      structure={child}
      depth={0}
      isMobile={true}
      onSelectLink={() => {
        setIsExpanded(false);
      }}
    />
  ));

  const darkModeButton = (
    <div>
      <style jsx>{`
        div {
          float: right; 
          margin-top: -8px;
        }
      }`}</style>
      <TrayButton
        onClick={toggleDarkMode}
        text={colorScheme == colors ? "Dark Mode" : "Light Mode"}
      />
    </div>
  );

  return isExpanded ? (
    <div className="container">
      <style jsx>{`
        .container {
          background-color: ${colorScheme.tray.background};
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
