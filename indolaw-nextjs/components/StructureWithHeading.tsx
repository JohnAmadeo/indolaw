import { CSSProperties } from "react";
import {
  Complex,
  Primitive,
  renderPenjelasan,
  renderStructure,
  Structure,
  NodeMap,
} from "utils/grammar";
import PrimitiveStructure from "./PrimitiveStructure";

export default function StructureWithHeading(props: {
  structure: Complex;
  numOfHeadingLines: number;
}): JSX.Element {
  const { structure, numOfHeadingLines } = props;
  const headingStyle: CSSProperties = {
    marginLeft: "0px",
    textAlign: "center",
    margin: "8px 0",
    fontWeight: 700,
  };

  const inPerubahanStructure = structure.type.includes('PERUBAHAN');

  return (
    <>
      <style jsx>{`
        div {
          margin: ${inPerubahanStructure ? '0' : '48px'} 0 0 0;
        }
      `}</style>
      <div id={structure.id}>
        {structure.children.slice(0, numOfHeadingLines).map((child, idx) => (
          <PrimitiveStructure
            key={idx}
            structure={child as Primitive}
            customStyle={headingStyle}
          />
        ))}
      </div>
      {structure.children.slice(numOfHeadingLines).map((child, idx) =>
        renderStructure(child, idx))}
    </>
  );
}
