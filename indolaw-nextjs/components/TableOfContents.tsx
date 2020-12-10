import { CSSProperties } from "react";
import { Structure, Complex, Primitive } from "utils/grammar";

/*
 * TODO(johnamadeo)
 * 2. Collapsible (can hide all child structures)
 * 3. Linking
 */

export default function TableOfContents(props: { law: Complex }): JSX.Element {
  return renderUndangUndang(props.law);
}

function renderStructure(
  structure: Complex | Primitive,
  depth: number
): JSX.Element {
  switch (structure.type) {
    case Structure.BAB:
    case Structure.BAGIAN:
    case Structure.PARAGRAF:
      return renderStructuresWithTitleAndNumber(structure as Complex, depth);
    case Structure.PASAL:
      return renderPasal(structure as Complex, depth);
    case Structure.LIST:
    case Structure.LIST_ITEM:
    case Structure.PLAINTEXT:
    case Structure.BAB_NUMBER:
    case Structure.BAB_TITLE:
    case Structure.PASAL_NUMBER:
    case Structure.BAGIAN_NUMBER:
    case Structure.BAGIAN_TITLE:
    case Structure.PARAGRAF_NUMBER:
    case Structure.PARAGRAF_TITLE:
    default:
      return <></>;
  }
}

function renderUndangUndang(structure: Complex): JSX.Element {
  return (
    <>{structure.children.map((children) => renderStructure(children, 0))}</>
  );
}

function renderStructuresWithTitleAndNumber(structure: Complex, depth: number) {
  const number = structure.children[0] as Primitive;
  const title = structure.children[1] as Primitive;
  return (
    <>
      {renderLink(`${number.text}: ${title.text}`, depth)}
      {structure.children
        .slice(2)
        .map((children) => renderStructure(children, depth + 1))}
    </>
  );
}

function renderPasal(structure: Complex, depth: number) {
  const number = structure.children[0] as Primitive;
  return (
    <>
      {renderLink(`${number.text}`, depth)}
      {structure.children
        .slice(2)
        .map((children) => renderStructure(children, depth + 1))}
    </>
  );
}

// TODO(johnamadeo): Add link
function renderLink(label: string, depth: number): JSX.Element {
  return (
    <p
      style={{
        marginLeft: `${depth * 28}px`,
        padding: "4px",
      }}
    >
      {label}
    </p>
  );
}
