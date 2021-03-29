import { CSSProperties } from "react";
import { Complex, Primitive, renderStructure } from "utils/grammar";
import CenteredHeading from "./CenteredHeading";
import PrimitiveStructure from "./PrimitiveStructure";

export default function Penjelasan(props: {
  structure: Complex;
}): JSX.Element {
  const { structure } = props;
  return (
    <>
      <style jsx>{`
        div {
          margin: 144px 0 0 0;
        }
      `}</style>
      <div>
        {/* PENJELASAN_TITLE */}
        {renderStructure(structure.children[0] as Complex)}
        {/* PENJELASAN_UMUM */}
        {renderStructure(structure.children[1] as Complex)}
        {/* PENJELASAN_PASAL_DEMI_PASAL */}
        {renderStructure(structure.children[2] as Complex)}
      </div>
    </>
  );
}
