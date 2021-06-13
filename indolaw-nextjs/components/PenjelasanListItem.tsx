import { Structure, Complex, Primitive, renderStructure } from "utils/grammar";
import PrimitiveStructure from "components/PrimitiveStructure";
import { useMediaQuery } from "react-responsive";

export default function PenjelasanListItem(props: { structure: Complex }): JSX.Element {
  const { structure } = props;
  const isMobile = useMediaQuery({ maxWidth: 768 });

  return (
    <div className="container">
      <style jsx>{`
        .container {
          margin: 8px 0;
        }

        .list-item {
          margin-left: 48px;
        }
      `}</style>
      <div>
        <PrimitiveStructure structure={structure.children[0] as Primitive} />
      </div>
      <div className="list-item">
        <div className="text-block">
          {structure.children.slice(1).map((childStructure, idx) =>
            renderStructure(childStructure, idx, [], isMobile)
          )}
        </div>
      </div>
    </div>
  );
}
