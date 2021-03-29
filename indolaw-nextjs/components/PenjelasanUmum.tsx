import { CSSProperties } from "react";
import { Complex, Primitive, renderStructure } from "utils/grammar";
import CenteredHeading from "./CenteredHeading";
import PrimitiveStructure from "./PrimitiveStructure";

export default function PenjelasanUmum(props: {
  structure: Complex;
}): JSX.Element {
  const { structure } = props;
  return (
    <>
      <style jsx>{`
        .block {
          margin: 16px 0 0 0;
        }
      `}</style>
      <div>
        {structure.children.map((child, idx) => (
          <div className="block" key={idx}>
            {renderStructure(child)}
          </div>
        ))}
      </div>
    </>
  );
}
