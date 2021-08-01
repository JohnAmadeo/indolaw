import { useState } from "react";
import { Structure, Complex, Primitive } from "utils/grammar";
import { colors, fonts } from "utils/theme";
import { NextRouter, useRouter } from "next/router";
import { useAppContext } from "../utils/context-provider";
import TableOfContentsGroupList from "./TableOfContentsGroupList";

export default function TableOfContentsGroup(props: {
  structure: Complex | Primitive,
  depth: number,
  isMobile: boolean,
  shouldShowExpanderWidth: boolean,
  onSelectLink?: () => void,
}): JSX.Element {
  const { structure, depth, isMobile, onSelectLink, shouldShowExpanderWidth } = props;
  const [isChildrenVisible, setIsChildrenVisible] = useState(false);
  const [isHoverOnHeading, setIsHoverOnHeading] = useState(false);
  const router = useRouter();
  const currentRoute = getRoute(router);
  const { colorScheme } = useAppContext();

  const children = getChildren(structure, depth + 1, isMobile, onSelectLink);
  const hasChildren = children !== null;

  const number = getNumber(structure);
  const title = getTitle(structure);
  if (title == null && number === null) {
    return <></>;
  }

  const base = 14;
  const px = (num: number) => `${num}px`;
  const style = {
    titleSize: px(base),
    numberSize: '14px',
    iconSize: '24px',
    iconMarginLeft: '-6px',
    iconMarginTop: '-4px',
    groupPaddingVert: px((1 / 4) * base),
  };

  const onSelectHeading = () => {
    if (!isMobile) {
      if (isLink(structure)) {
        router.push(`${currentRoute}#${structure.id}`);
      }
    } else {
      if (isLink(structure) && !hasChildren) {
        if (onSelectLink) {
          onSelectLink();
        }
        router.push(`${currentRoute}#${structure.id}`);
      } else {
        setIsChildrenVisible(!isChildrenVisible);
      }
    }
  };

  const onSelectExpander = () => {
    if (!isMobile) {
      setIsChildrenVisible(!isChildrenVisible);
    }
  };

  return (
    <div className="container">
      <style jsx>{`
        .container {
          display: flexbox;
          margin: 2px 16px 2px 0;
          width: 100%;
        }

        .expander {
          padding: 22px 0 0 0;
          width: 18px;
        }

        .heading-container {
          flex-grow: 1;
          width: 100%;
        }

        .heading {
          color: ${isHoverOnHeading ? colorScheme.clickable : colors.tray.text};
          font-family: ${fonts.sans};
          padding: ${style.groupPaddingVert} 8px;
          cursor: ${isMobile ? "pointer" : "auto"};
          border-radius: 8px;
          cursor: ${isMobile || isLink(structure) ? "pointer" : "auto"};
        }

        .heading:hover {
          background: ${colorScheme.clickableBackground};
        }

        .number {
          font-size: ${style.numberSize};
          color: ${colorScheme.tray.textSecondary};
        }

        .title {
          font-size: ${style.titleSize};
        }

        .material-icons.style {
          font-size: ${style.iconSize};
          margin-left: ${style.iconMarginLeft};
          margin-top: ${style.iconMarginTop};
          cursor: pointer;
          vertical-align: bottom;
          color: ${colorScheme.clickable};
        }

        .children {
          margin-left: 8px;
        }
      `}</style>
      {shouldShowExpanderWidth && (
        <div className="expander" onClick={onSelectExpander}>
          {hasChildren && (
            <i className="material-icons style">
              {isChildrenVisible ? "expand_less" : "expand_more"}
            </i>
          )}
        </div>
      )}
      <div className="heading-container">
        <div className="heading"
          onClick={onSelectHeading}
          onMouseEnter={() => setIsHoverOnHeading(true)}
          onMouseLeave={() => setIsHoverOnHeading(false)}
        >
          <div className="number">{number}</div>
          <div className="title">
            {title}
          </div>
        </div>
        {hasChildren && isChildrenVisible && (
          <div className="children">{children}</div>
        )}
      </div>
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
      return <TableOfContentsGroupList structures={(structure as Complex).children.slice(2)} />;
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