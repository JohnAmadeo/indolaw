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
          background-color: ${colorScheme.subcontent};
          padding: 10px 20px;
          border-radius: 7.5px;
        }

        .title {
          margin: 8px 0;
          font-weight: 700;
          line-height: 1.5;
          display: flex;
          justify-content: center;
        }
      `}</style>
      <div className="group">
        <div
          className="title"
          onClick={() => setIsContentVisible(!isContentVisible)}
        >
          {
            <i className="material-icons style">
              {isContentVisible ? "expand_less" : "expand_more"}
            </i>
          }
          <span> Penjelasan </span>
        </div>

        {isContentVisible && (
          <div>
            {/*                             
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
          </div> */}

            {structure.children.slice(numOfHeadingLines).map((child, idx) => {
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
