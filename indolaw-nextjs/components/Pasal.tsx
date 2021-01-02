import { Complex, Primitive, renderStructure } from "utils/grammar";
import PrimitiveStructure from "components/PrimitiveStructure";
import { CSSProperties } from "react";

export default function Pasal(props: { structure: Complex }): JSX.Element {
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
      </div>
      {structure.children.slice(1).map(renderStructure)}
    </>
  );
}
