import { Structure, Complex, Primitive, renderStructure } from "utils/grammar";
import PrimitiveStructure from "components/PrimitiveStructure";
import { useMediaQuery } from "react-responsive";

export default function ListItem(props: { structure: Complex }): JSX.Element {
  const { structure } = props;
  const isDesktop = useMediaQuery({ query: "(min-width: 768px)" });

  return (
    <div className="list-item">
      <style jsx>{`
        .list-item {
          display: flex;
          margin: 4px 0;
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
        {structure.children.map((childStructure) => {
          if (childStructure.type === Structure.PLAINTEXT) {
            return (
              <PrimitiveStructure
                structure={childStructure as Primitive}
                customStyle={{
                  textAlign: isDesktop ? "justify" : "start",
                }}
              />
            );
          }

          return renderStructure(childStructure);
        })}
      </div>
    </div>
  );
}
