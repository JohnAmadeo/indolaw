import { useState } from "react";
import { Complex } from "utils/grammar";
import { colors, darkColors, fonts } from "utils/theme";
import TableOfContentsGroup from "components/TableOfContentsGroup";
import { useMediaQuery } from "react-responsive";

export default function TableOfContents(props: { 
  law: Complex,
  isDarkMode: boolean,
  setIsDarkMode: () => void
 }): JSX.Element {
  const {isDarkMode, setIsDarkMode} = props;
  const isMobile = useMediaQuery({ query: "(max-width: 768px)" });
  const [isExpanded, setIsExpanded] = useState(false);

  const tableOfContents = props.law.children.map((child, idx) => (
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

  const darkModeButton = (<><style>{
      `button {
        width: 25%;
        height: 3vh;
        margin-bottom: 10px;
        background-color: ${(isDarkMode ? colors : darkColors).trayBackground}; // get the inverse for dark mode button
        border-radius: 7px;
        border: 0;
        color: ${(isDarkMode ? colors : darkColors).dark.text};
        font-family: ${fonts.sans};
        ${isMobile ? "float: right;" : "margin-left: auto; display: block;"}
      }
      }`}</style><button onClick={setIsDarkMode}>{isDarkMode ? "Light Mode" : "Dark Mode"}</button></>
  );

  if (!isMobile) {
    return <>
      {darkModeButton}
      {tableOfContents}
    </>;
  }

  return isExpanded ? (
    <div className="container">
      <style jsx>{`
        .container {
          background-color: ${(isDarkMode ? darkColors : colors).trayBackground};
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
          border-bottom: 1px solid ${(isDarkMode ? darkColors : colors).dark.text};
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
          color: ${(isDarkMode ? darkColors : colors).dark.text};
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
          color: ${(isDarkMode ? darkColors : colors).dark.text};
        }

        .material-icons.style {
          vertical-align: bottom;
        }
      `}</style>
        <span onClick={() => {
            setIsExpanded(true);
          }}>
          <i  className="material-icons style">expand_more</i> Daftar Isi     
        </span>
      {darkModeButton}
      </>
    );
}
