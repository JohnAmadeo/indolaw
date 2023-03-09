import { Complex, LawData, Primitive, Structure } from "utils/grammar";
import Law from "components/Law";
import { MutableRefObject, useRef, useState } from "react";
import { useAppContext, VisibilityContext } from "../utils/context-provider";
import Tray from "./Tray";
import LawPageMetadataCard from "./LawPageMetadataCard";
import { fonts } from "utils/theme";
import LawPagePdfDownloadCard from "./LawPagePdfDownloadCard";

type VisibilityMap = {
  [id: string]: {
    element: HTMLElement | null,
    isVisible: boolean,
  }
};

// TODO(johnamadeo): Fix "Warning: Each child in a list should have a unique "key" prop." problem
export default function DesktopLawPage(props: {
  law: LawData;
}): JSX.Element {
  const [isTrayExpanded, setIsTrayExpanded] = useState(true);
  const { colorScheme } = useAppContext();
  const { year, number, topic, bpkPdfLink, bpkLink } = props.law.metadata;
  const { content } = props.law;

  const expandedTrayWidth = 320;
  // Ideally we'd want to set the width of the minimized tray to just 'inherit' so that it'll be as
  // wide as its contents; however in order to animate the tray collapsing/expanding we cannot use
  // 'inherit' due to a CSS transition limitation. See https://css-tricks.com/using-css-transitions-auto-dimensions/
  const minimizedTrayWidth = 44;
  const trayWidth = isTrayExpanded ? expandedTrayWidth : minimizedTrayWidth;
  const mainBodyWidth = 816;
  const variableWidthThreshold = 1224;

  const nameAndYear = `UU No. ${number} Tahun ${year}`;
  const topicText = `Tentang ${topic}`;

  const visibilityRef = useRef(extractPasalMap(props.law.content));
  const lawContainerRef: MutableRefObject<HTMLDivElement | null> = useRef(null);

  const getTopmostVisibleElement = () => {
    let topY = Infinity;
    let topElement: HTMLElement | null = null;
    for (let pasal of Object.values(visibilityRef.current)) {
      if (!pasal.isVisible) {
        continue;
      }

      const y = pasal.element?.getBoundingClientRect().y;
      if (y != null && y < topY && y > -10) {
        topY = y;
        topElement = pasal.element;
      }
    }

    return topElement;
  };

  const maybeScrollToElement = (element: HTMLElement | null) => {
    const isVariableWidth =
      lawContainerRef.current != null &&
      lawContainerRef.current.clientWidth < variableWidthThreshold;

    if (isVariableWidth) {
      setTimeout(() => {
        element?.scrollIntoView();
      }, 200);
    }
  };

  return (
    <div className="container">
      <style jsx>{`
        .container {
          display: flex;
          background-color: ${colorScheme.background};
        }

        .law-container {
          flex-grow: 1;
          max-width: calc(100% - ${trayWidth}px);
          transition: max-width ease 0.2s;
        }

        .name-and-year {
          margin: 12px 0 0 0;
          font-family: ${fonts.serif};
          font-size: 48px;
          color: ${colorScheme.text};
        }
        
        .topic {
          margin: 0 0 24px 0;
          font-family: ${fonts.serif};
          font-size: ${topicText.length > 60 ? '26px' : '48px'};
          color: ${colorScheme.text};
        }

        .law {
          margin: 24px auto 0 auto;
          width: ${mainBodyWidth}px;
        }

        .cards {
          width: ${mainBodyWidth}px;
          margin: 24px auto;
        }

        @media screen and (max-width: ${variableWidthThreshold}px) {
          .law {
            width: auto;
            padding: 0 24px;
          }

          .cards {
            width: auto;
            padding: 0 24px;
          }
        }
      `}</style>
      <VisibilityContext.Provider
        value={{
          setElement: (id: string, element: HTMLElement) => {
            if (id in visibilityRef.current) {
              visibilityRef.current[id] = {
                element,
                isVisible: visibilityRef.current[id].isVisible,
              }
            }
          },
          setIsVisible: (id: string, isVisible: boolean) => {
            if (id in visibilityRef.current) {
              visibilityRef.current[id] = {
                element: visibilityRef.current[id].element,
                isVisible,
              }
            }
          },
        }}
      >
        <Tray
          law={props.law}
          isExpanded={isTrayExpanded}
          onExpand={() => {
            const topElement = getTopmostVisibleElement();
            setIsTrayExpanded(true);
            maybeScrollToElement(topElement);
          }}
          onMinimize={() => {
            const topElement = getTopmostVisibleElement();
            setIsTrayExpanded(false);
            maybeScrollToElement(topElement);
          }}
          width={trayWidth}
        />

        <div className="law-container">
          <div className="cards">
            <h1 className="name-and-year">{nameAndYear}</h1>
            <h1 className="topic">{topicText}</h1>
            <LawPageMetadataCard metadata={props.law.metadata} />
          </div>
          {content == null ? (
            <div className="cards">
              <LawPagePdfDownloadCard
                lawNameAndYear={nameAndYear}
                pdfLink={bpkPdfLink}
                webpageLink={bpkLink}
              />
            </div>
          ) : (
            <div className="law" ref={lawContainerRef}>
              <Law law={content} metadata={props.law.metadata} colorScheme={colorScheme} />
            </div>
          )}
        </div>
      </VisibilityContext.Provider>
    </div>
  );
}

function extractPasalMap(law: Complex | null | undefined): VisibilityMap {
  const pasalMap: VisibilityMap = {};
  if (law == null) {
    return pasalMap;
  }

  const traverse = (structure: Complex | Primitive) => {
    if (structure != null && "children" in structure && structure.children !== undefined) {
      structure = structure as Complex;

      if (structure.type === Structure.PASAL) {
        pasalMap[structure.id] = {
          isVisible: false,
          element: null,
        };
      } else {
        for (let child of structure.children) {
          traverse(child);
        }
      }
    }
  }

  traverse(law);
  return pasalMap;
}