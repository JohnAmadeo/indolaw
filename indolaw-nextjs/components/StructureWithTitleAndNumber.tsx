import { CSSProperties } from "react";
import { Complex, Primitive, renderStructure } from "utils/grammar";
import PrimitiveStructure from "./PrimitiveStructure";

export default function StructureWithTitleAndNumber(props: {
  structure: Complex;
}): JSX.Element {
  const { structure } = props;
  const headingStyle: CSSProperties = {
    marginLeft: "0px",
    textAlign: "center",
    margin: "8px 0",
  };

  return (
    <>
      <style jsx>{`
        div {
          margin: 48px 0 0 0;
        }
      `}</style>
      <div id={structure.id}>
        <PrimitiveStructure
          structure={structure.children[0] as Primitive}
          customStyle={headingStyle}
        />
        <PrimitiveStructure
          structure={structure.children[1] as Primitive}
          customStyle={headingStyle}
        />
      </div>
      {structure.children.slice(2).map(renderStructure)}
    </>
  );
}
