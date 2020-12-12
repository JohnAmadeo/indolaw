import { CSSProperties } from "react";
import { Structure, Complex, Primitive } from "utils/grammar";

// TODO(johnamadeo): Fix "Warning: Each child in a list should have a unique "key" prop." problem
export default function Law(props: { law: Complex }): JSX.Element {
  return (
    <>
      <h1>UNDANG UNDANG REPUBLIK INDONESIA TENTANG CIPTA KERJA</h1>
      {renderUndangUndang(props.law)}
    </>
  );
}

function renderStructure(structure: Complex | Primitive) {
  switch (structure.type) {
    case Structure.PLAINTEXT:
    case Structure.BAB_NUMBER:
    case Structure.BAB_TITLE:
    case Structure.PASAL_NUMBER:
    case Structure.BAGIAN_NUMBER:
    case Structure.BAGIAN_TITLE:
    case Structure.PARAGRAF_NUMBER:
    case Structure.PARAGRAF_TITLE:
      return renderPrimitive(structure as Primitive);
    case Structure.BAB:
    case Structure.BAGIAN:
    case Structure.PARAGRAF:
      return renderStructuresWithTitleAndNumber(structure as Complex);
    case Structure.LIST:
      return renderList(structure as Complex);
    case Structure.LIST_ITEM:
      return renderListItem(structure as Complex);
    case Structure.PASAL:
      return renderPasal(structure as Complex);
    default:
      return <></>;
  }
}

function renderPrimitive(
  structure: Primitive,
  customStyle: CSSProperties = {}
): JSX.Element {
  let style: CSSProperties = {
    margin: "4px 0",
    fontSize: "18px",
    // border: "1px solid red",
  };

  return (
    <div style={{ ...style, ...customStyle }}>
      <p>{structure.text}</p>
    </div>
  );
}

// TODO(johnamadeo): I think there are multi-line titles later on in the text
function renderStructuresWithTitleAndNumber(structure: Complex): JSX.Element {
  const style: CSSProperties = {
    margin: "48px 0",
  };
  const headingStyle: CSSProperties = {
    marginLeft: "0px",
    textAlign: "center",
    margin: "8px 0",
  };

  return (
    <>
      <div style={style} id={structure.id}>
        {renderPrimitive(structure.children[0] as Primitive, headingStyle)}
        {renderPrimitive(structure.children[1] as Primitive, headingStyle)}
      </div>
      {structure.children
        .slice(2)
        .map((childStructure) => renderStructure(childStructure))}
    </>
  );
}

function renderList(structure: Complex): JSX.Element {
  return (
    <div>
      {structure.children.map((childStructure) =>
        renderStructure(childStructure)
      )}
    </div>
  );
}

function renderListItem(structure: Complex): JSX.Element {
  // TODO(johnamadeo): Decide how the heck we wanna do CSS (CSS modules, big CSS object at bottom?)
  return (
    <div
      style={{
        display: "flex",
        margin: "4px 0",
      }}
    >
      <div
        style={{
          minWidth: "48px",
        }}
      >
        {renderPrimitive(structure.children[0] as Primitive)}
      </div>
      <div
        style={{
          flexGrow: 1,
        }}
      >
        {structure.children.map((childStructure) => {
          if (childStructure.type === Structure.PLAINTEXT) {
            return renderPrimitive(childStructure as Primitive, {
              textAlign: "justify",
            });
          }

          return renderStructure(childStructure);
        })}
      </div>
    </div>
  );
}

function renderPasal(structure: Complex): JSX.Element {
  const style: CSSProperties = {
    margin: "48px 0 0 0",
  };
  const headingStyle: CSSProperties = {
    marginLeft: "0px",
    textAlign: "center",
    margin: "8px 0",
  };
  return (
    <>
      <div style={style} id={structure.id}>
        {renderPrimitive(structure.children[0] as Primitive, headingStyle)}
      </div>
      {structure.children
        .slice(1)
        .map((childStructure) => renderStructure(childStructure))}
    </>
  );
}

function renderUndangUndang(structure: Complex): JSX.Element {
  return <>{structure.children.map((children) => renderStructure(children))}</>;
}
