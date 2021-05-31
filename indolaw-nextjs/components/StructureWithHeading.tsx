import { CSSProperties } from "react";
import { Complex, Primitive, renderPenjelasanUmum, renderStructure, Structure } from "utils/grammar";
import PrimitiveStructure from "./PrimitiveStructure";

export default function StructureWithHeading(props: {
  structure: Complex;
  penjelasanUmum?: Array<Complex | Primitive>;
  numOfHeadingLines: number;
}): JSX.Element {
  const { structure, numOfHeadingLines, penjelasanUmum } = props;
  const headingStyle: CSSProperties = {
    marginLeft: "0px",
    textAlign: "center",
    margin: "8px 0",
    fontWeight: 700,
  };

  return (
    <>
      <style jsx>{`
        div {
          margin: 48px 0 0 0;
        }
      `}</style>
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
      {structure.children
        .slice(numOfHeadingLines)
        .map((child, idx) => {
          let result = [renderStructure(child, idx, penjelasanUmum)];

          if (child.type === Structure.PASAL && penjelasanUmum) {
            const penjelasanUmumNode = penjelasanUmum.shift();
            if (penjelasanUmumNode) {
              result.push(renderPenjelasanUmum(penjelasanUmumNode));
            }
          }

          return result;
        })}
    </>
  );
}
