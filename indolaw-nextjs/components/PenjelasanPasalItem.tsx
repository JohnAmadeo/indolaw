import { CSSProperties, useState } from "react";
import { Complex, Primitive, renderStructure } from "utils/grammar";
import { useAppContext } from "../utils/context-provider";
import PrimitiveStructure from "./PrimitiveStructure";

export default function PenjelasanPasalItem(props: {
  structure: Complex;
  numOfHeadingLines: number;
}): JSX.Element {
  const { structure, numOfHeadingLines } = props;
  const [isContentVisible, setIsContentVisible] = useState(false);
  const { colorScheme } = useAppContext();

  const headingStyle: CSSProperties = {
    marginLeft: "0px",
    textAlign: "center",
    margin: "8px 0",
    fontWeight: 700,
  };

  return (
    <>
      <style jsx>{`
        .group {
          margin: 20px auto;
          background-color: ${colorScheme.subcontent.background};
          padding: 10px 20px;
          border-radius: 7.5px;
        }

        .group:hover {
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
      `}</style>
      <div
        className="group"
        onClick={() => setIsContentVisible(!isContentVisible)}
      >
        <div className="title">
          {
            <i className="material-icons style">
              {isContentVisible ? "expand_less" : "expand_more"}
            </i>
          }
          <span> Penjelasan </span>
        </div>

        {isContentVisible && (
          <div className="content">
            <div id={structure.id}>
              {structure.children
                .slice(0, numOfHeadingLines)
                .map((child, idx) => (
                  <PrimitiveStructure
                    key={idx}
                    structure={child as Primitive}
                    customStyle={headingStyle}
                  />
                ))}
            </div>

            {structure.children.slice(numOfHeadingLines).map((child, idx) => {
              // The if-statement below should be temporary, as the current parser parses "TAMBAHAN xxxx" as part of penjelasan
              // which should not be the intended behavior
              if (
                (child as Primitive).text &&
                (child as Primitive).text.startsWith(
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
