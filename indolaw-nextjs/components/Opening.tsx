import { CSSProperties } from "react";
import { Complex, Primitive, renderStructure } from "utils/grammar";
import CenteredHeading from "./CenteredHeading";
import PrimitiveStructure from "./PrimitiveStructure";

export default function Opening(props: {
  structure: Complex;
}): JSX.Element {
  const { structure } = props;
  const headingStyle: CSSProperties = {
    marginLeft: "0px",
    textAlign: "center",
    margin: "8px 0",
  };

  // TODO(johnamadeo): CONSIDERATIONS & PRINCIPLES needs more vertical margin
  return (
    <>
      <style jsx>{`
        div {
          margin: 48px 0 0 0;
        }
      `}</style>
      {/* UU_TITLE */}
      <CenteredHeading structure={structure.children[0] as Complex} />
      {/* PREFACE */}
      <CenteredHeading structure={structure.children[1] as Complex} />
      {/* CONSIDERATIONS */}
      {renderStructure(structure.children[2] as Complex)}
      {/* PRINCIPLES */}
      {renderStructure(structure.children[3] as Complex)}
      {/* AGREEMENT - TODO(johnamadeo): Menetapkan should be rendered paragraph style not centered */}
      <CenteredHeading structure={structure.children[4] as Complex} />
    </>
  );
}
