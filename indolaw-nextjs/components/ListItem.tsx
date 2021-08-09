import { Structure, Complex, Primitive, renderStructure } from "utils/grammar";
import PrimitiveStructure from "components/PrimitiveStructure";
import { useMediaQuery } from "react-responsive";
import { useIsMobile } from "utils/hooks";

export default function ListItem(props: { structure: Complex }): JSX.Element {
  const { structure } = props;
  const isMobile = useIsMobile();

  return (
    <div className="list-item">
      <style jsx>{`
        .list-item {
          display: flex;
        }

        .list-index {
          min-width: 48px;
        }

        .text-block {
          flex-grow: 1;
        }
      `}</style>
      <div className="list-index">
        <PrimitiveStructure structure={structure.children[0] as Primitive} />
      </div>
      <div className="text-block">
        {structure.children.slice(1).map((childStructure, idx) =>
          renderStructure(childStructure, idx, isMobile)
        )}
      </div>
    </div>
  );
}
