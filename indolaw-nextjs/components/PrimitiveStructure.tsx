import { CSSProperties } from "react";
import { Primitive } from "utils/grammar";

export default function PrimitiveStructure(props: {
  structure: Primitive;
  customStyle?: CSSProperties;
}): JSX.Element {
  const { structure, customStyle } = props;
  return (
    <div style={{ ...customStyle }}>
      <style jsx>{`
        div {
          margin: 4px 0;
          font-size: 18px;
          // border: "1px solid red";
        }
      `}</style>
      <p>{structure.text}</p>
    </div>
  );
}
