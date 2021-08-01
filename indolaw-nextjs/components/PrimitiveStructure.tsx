import { CSSProperties, useState } from "react";
import { Primitive, Structure } from "utils/grammar";
import { useAppContext } from "utils/context-provider";
import { emptyTooltipData, TooltipData } from "./Tooltip";
import Tooltip from "./Tooltip";

export default function PrimitiveStructure(props: {
  structure: Primitive;
  customStyle?: CSSProperties;
}): JSX.Element {
  const {
    structure: { text, type },
    customStyle,
  } = props;

  const [tooltipData, setTooltipData] = useState(emptyTooltipData);

  return (
    <>
      <div style={{ ...customStyle }}>
        <style jsx>{`
        div {
          margin: 4px 0 16px 0;
        }

        p {
          line-height: 1.5;
        }
      `}</style>
        <p>{type === Structure.PLAINTEXT ? sanitizeKetentuanUmum(text, setTooltipData) : text}</p>
      </div>
      <Tooltip tooltipData={tooltipData} />
    </>
  );
}

function sanitizeKetentuanUmum(
  text: string,
  setTooltipData: (data: TooltipData) => void,
): string | Array<JSX.Element> {
  // Sanitize law from ketentuan umum identifier

  const regex = /(\${[^}]*})/;
  const spans = text.split(regex);

  if (spans.length === 1) {
    return text;
  }

  const { colorScheme } = useAppContext();

  let linkedSpans = [];
  for (let i = 0; i < spans.length; i++) {
    const isLinkable = spans[i].match(regex) != null;
    if (isLinkable) {
      const word = spans[i].substring(2, spans[i].length - 1);
      linkedSpans.push(
        <span
          key={i}
          className="link"
          onPointerOver={(e) => {
            setTooltipData({
              contentKey: word,
              xPosition: e.currentTarget.offsetLeft,
              yPosition:
                e.currentTarget.offsetTop + e.currentTarget.offsetHeight + 8,
            });
          }}
          onPointerLeave={() => {
            setTooltipData(emptyTooltipData);
          }}
        >
          <style jsx>{`
            .link {
              border-bottom: 1px dashed ${colorScheme.clickable};
            }

            .link:hover {
              background: ${colorScheme.clickableBackground};
              cursor: pointer;
            }
          `}</style>
          {word}
        </span>
      );
    } else {
      linkedSpans.push(<span key={i}>{spans[i]}</span>);
    }
  }

  return linkedSpans;
}
