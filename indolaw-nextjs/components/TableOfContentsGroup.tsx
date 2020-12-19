import { useState } from "react";
import { Structure, Complex, Primitive } from "utils/grammar";
import Link from "next/link";
import { colors, fonts } from "utils/theme";

export default function TableOfContentsGroup(props: {
  structure: Complex | Primitive;
  depth: number;
  isMobile: boolean;
}): JSX.Element {
  const { structure, depth, isMobile } = props;
  const [isChildrenVisible, setIsChildrenVisible] = useState(false);

  const children = getChildren(structure, depth + 1, isMobile);
  const hasChildren = children !== null;

  const number = getNumber(structure);
  const title = getTitle(structure);
  if (title == null && number === null) {
    return <></>;
  }

  const px = (num: number) => `${num}px`;
  const anchor = 18;
  const style = {
    titleSize: px(anchor),
    numberSize: px((4 / 5) * anchor),
    iconSize: px((4 / 3) * anchor),
    iconMarginLeft: px((-1 / 4) * anchor),
    groupMarginTop: px((1 / 2) * anchor),
  };

  return (
    <div>
      <style jsx>{`
        .group {
          display: grid;
          grid-template-columns: ${style.iconSize} 1fr;
          margin-top: ${style.groupMarginTop};
          color: ${colors.dark.text};
          font-family: ${fonts.sans};
        }

        .group div {
          // border: 1px solid blue;
        }

        .number {
          font-size: ${style.numberSize};
          color: ${colors.dark.textSecondary};
        }

        .title {
          font-size: ${style.titleSize};
        }

        .title:hover {
          color: ${isLink(structure) ? colors.text : colors.dark.text};
        }

        .material-icons.style {
          font-size: ${style.iconSize};
          margin-left: ${style.iconMarginLeft};
          cursor: pointer;
          vertical-align: bottom;
          // border: 1px solid red;
        }

        .children {
          margin-left: ${style.iconSize};
          margin-top: ${style.groupMarginTop};
        }
      `}</style>
      <div className="group">
        <div></div>
        <div className="number">{number}</div>
        <div onClick={() => setIsChildrenVisible(!isChildrenVisible)}>
          {hasChildren && (
            <i className="material-icons style">
              {isChildrenVisible ? "expand_less" : "expand_more"}
            </i>
          )}
        </div>
        <div className="title">
          {isLink(structure) ? (
            <Link href={`/laws/test#${structure.id}`}>{title}</Link>
          ) : (
            title
          )}
        </div>
      </div>
      {hasChildren && isChildrenVisible && (
        <div className="children">{children}</div>
      )}
    </div>
  );
}

function getChildren(
  structure: Complex | Primitive,
  depth: number,
  isMobile: boolean
): JSX.Element | null {
  switch (structure.type) {
    case Structure.BAB:
    case Structure.BAGIAN:
    case Structure.PARAGRAF:
      return (
        <>
          {(structure as Complex).children.slice(2).map((child) => (
            <TableOfContentsGroup
              structure={child}
              depth={depth + 1}
              isMobile={isMobile}
            />
          ))}
        </>
      );
    default:
      return null;
  }
}

function getTitle(structure: Complex | Primitive): string | null {
  switch (structure.type) {
    case Structure.BAB:
    case Structure.BAGIAN:
    case Structure.PARAGRAF:
      const title = (structure as Complex).children[1] as Primitive;
      return toTitleCase(title.text);
    case Structure.PASAL:
      return ((structure as Complex).children[0] as Primitive).text;
    default:
      return null;
  }
}

function getNumber(structure: Complex | Primitive): string | null {
  switch (structure.type) {
    case Structure.BAB:
    case Structure.BAGIAN:
    case Structure.PARAGRAF:
      const number = (structure as Complex).children[0] as Primitive;
      return toTitleCase(number.text);
    default:
      return null;
  }
}

function toTitleCase(str: string) {
  return str
    .split(" ")
    .map((word) => {
      // if it's a roman numeral, don't convert it to titlecase
      return word.match("^[MDCLXVI]+$") !== null
        ? word
        : word.charAt(0).toUpperCase() + word.substr(1).toLowerCase();
    })
    .join(" ");
}

function isLink(structure: Complex | Primitive): structure is Complex {
  return "id" in structure && structure.id !== "";
}
