import { useState } from "react";
import { Structure, Complex, Primitive } from "utils/grammar";
import { colors, fonts } from "utils/theme";
import { NextRouter, useRouter } from "next/router";

export default function TableOfContentsGroup(props: {
  structure: Complex | Primitive;
  depth: number;
  isMobile: boolean;
  onSelectLink?: () => void;
}): JSX.Element {
  const { structure, depth, isMobile, onSelectLink } = props;
  const [isChildrenVisible, setIsChildrenVisible] = useState(false);
  const router = useRouter();
  const currentRoute = getRoute(router);

  const children = getChildren(structure, depth + 1, isMobile, onSelectLink);
  const hasChildren = children !== null;

  const number = getNumber(structure);
  const title = getTitle(structure);
  if (title == null && number === null) {
    return <></>;
  }

  const base = 18;
  const px = (num: number) => `${num}px`;
  const style = {
    titleSize: px(base),
    numberSize: px((4 / 5) * base),
    iconSize: px((4 / 3) * base),
    iconMarginLeft: px((-1 / 4) * base),
    groupPaddingVert: px((1 / 4) * base),
  };

  const onSelectGroup = () => {
    if (!isMobile) {
      return;
    }

    if (isLink(structure) && !hasChildren) {
      if (onSelectLink) {
        onSelectLink();
      }
      router.push(`${currentRoute}#${structure.id}`);
    } else {
      setIsChildrenVisible(!isChildrenVisible);
    }
  };
  const onSelectTitle = () => {
    if (!isMobile && isLink(structure)) {
      router.push(`${currentRoute}#${structure.id}`);
    }
  };
  const onSelectExpander = () => {
    if (!isMobile) {
      setIsChildrenVisible(!isChildrenVisible);
    }
  };

  return (
    <div>
      <style jsx>{`
        .group {
          display: grid;
          grid-template-columns: ${style.iconSize} 1fr;
          color: ${colors.tray.text};
          font-family: ${fonts.sans};
          padding: ${style.groupPaddingVert};
          cursor: ${isMobile ? "pointer" : "auto"};
        }

        .group div {
          // border: 1px solid blue;
        }

        .number {
          font-size: ${style.numberSize};
          color: ${colors.tray.textSecondary};
        }

        .title {
          font-size: ${style.titleSize};
          cursor: ${isMobile || isLink(structure) ? "pointer" : "auto"};
        }

        .title:hover {
          color: ${!isMobile && isLink(structure)
          ? colors.text
          : colors.tray.text};
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
        }
      `}</style>
      <div className="group" onClick={onSelectGroup}>
        <div></div>
        <div className="number">{number}</div>
        <div onClick={onSelectExpander}>
          {hasChildren && (
            <i className="material-icons style">
              {isChildrenVisible ? "expand_less" : "expand_more"}
            </i>
          )}
        </div>
        <div className="title" onClick={onSelectTitle}>
          {title}
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
  isMobile: boolean,
  onSelectLink?: () => void
): JSX.Element | null {
  switch (structure.type) {
    case Structure.BAB:
    case Structure.BAGIAN:
    case Structure.PARAGRAF:
      return (
        <>
          {(structure as Complex).children.slice(2).map((child, idx) => (
            <TableOfContentsGroup
              key={idx}
              structure={child}
              depth={depth + 1}
              isMobile={isMobile}
              onSelectLink={onSelectLink}
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
    case Structure.PENJELASAN:
      return 'Penjelasan';
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

function getRoute(router: NextRouter): string {
  const number = router.query.number as string;
  const yearOrNickname = router.query.yearOrNickname as string;
  return router.route
    .replace('[number]', number)
    .replace('[yearOrNickname]', yearOrNickname);
}