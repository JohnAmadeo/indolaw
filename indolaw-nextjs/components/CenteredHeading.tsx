import { CSSProperties } from "react";
import { Complex, Primitive, renderStructure } from "utils/grammar";
import PrimitiveStructure from "./PrimitiveStructure";

export default function CenteredHeading(props: {
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
        {structure.children.map(child => (
          <PrimitiveStructure
            structure={child as Primitive}
            customStyle={headingStyle}
          />
        ))}
      </div>
    </>
  );
}
