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
    </>
  );
}
