import { CSSProperties, Props, ReactNode, useState } from "react";
import { Structure, Complex, Primitive } from "utils/grammar";
import Link from "next/link";

/*
 * TODO(johnamadeo)
 * 3. Linking
 */

export default function TableOfContents(props: { law: Complex }): JSX.Element {
  return (
    <>
      {props.law.children.map((child) => (
        <TableOfContentsGroup structure={child} depth={0} />
      ))}
    </>
  );
}

function TableOfContentsGroup(props: {
  structure: Complex | Primitive;
  depth: number;
}): JSX.Element {
  const { structure, depth } = props;
  const [isChildrenVisible, setIsChildrenVisible] = useState(false);

  const children = getChildren(structure, depth + 1);

  const labelText = getLabel(structure);
  if (labelText === null) {
    return <></>;
  }

  const labelLink =
    "id" in structure && structure.id !== "" ? (
      <Link href={`/laws/test#${structure.id}`}>{labelText}</Link>
    ) : (
      labelText
    );

  const expander =
    children !== null ? (
      <span onClick={() => setIsChildrenVisible(!isChildrenVisible)}>
        [{isChildrenVisible ? "-" : "+"}]
      </span>
    ) : null;

  return (
    <>
      <p
        style={{
          marginLeft: `${depth * 14}px`,
          padding: "6px 4px",
        }}
      >
        {expander} {labelLink}
      </p>
      {isChildrenVisible && children}
    </>
  );
}

function getChildren(
  structure: Complex | Primitive,
  depth: number
): JSX.Element | null {
  switch (structure.type) {
    case Structure.BAB:
    case Structure.BAGIAN:
    case Structure.PARAGRAF:
      return (
        <>
          {(structure as Complex).children.slice(2).map((child) => (
            <TableOfContentsGroup structure={child} depth={depth + 1} />
          ))}
        </>
      );
    case Structure.PASAL:
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
      return null;
  }
}

function getLabel(structure: Complex | Primitive): string | null {
  switch (structure.type) {
    case Structure.BAB:
    case Structure.BAGIAN:
    case Structure.PARAGRAF:
      const number = (structure as Complex).children[0] as Primitive;
      const title = (structure as Complex).children[1] as Primitive;
      return `${number.text}: ${title.text}`;
    case Structure.PASAL:
      return ((structure as Complex).children[0] as Primitive).text;
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
      return null;
  }
}
