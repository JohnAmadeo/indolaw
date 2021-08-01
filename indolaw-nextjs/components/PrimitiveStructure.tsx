import { CSSProperties } from "react";
import { Primitive, Structure } from "utils/grammar";
import Link from "next/link";
import { useAppContext } from "utils/context-provider";
import { emptyTooltip } from "../utils/tooltip";

export default function PrimitiveStructure(props: {
  structure: Primitive;
  customStyle?: CSSProperties;
}): JSX.Element {
  const {
    structure: { text, type },
    customStyle,
  } = props;

  return (
    <div style={{ ...customStyle }}>
      <style jsx>{`
        div {
          margin: 4px 0 16px 0;
        }

        p {
          line-height: 1.5;
        }
      `}</style>
      {/* <p>{text}</p> */}
      <p>{type === Structure.PLAINTEXT ? sanitizeKetentuanUmum(text) : text}</p>
    </div>
  );
}

function sanitizeKetentuanUmum(text: string): string | Array<JSX.Element> {
  // Sanitize law from ketentuan umum identifier

  const regex = /(\${[^}]*})/;
  const spans = text.split(regex);

  if (spans.length === 1) {
    return text;
  }

  const { colorScheme, setTooltip } = useAppContext();

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
            setTooltip({
              contentKey: word,
              xPosition: e.currentTarget.offsetLeft,
              yPosition:
                e.currentTarget.offsetTop + e.currentTarget.offsetHeight,
            });
          }}
          onPointerLeave={() => {
            setTooltip(emptyTooltip);
          }}
        >
          <style jsx>{`
            .link {
              color: ${colorScheme.linkText};
              border-bottom: 1px dashed;
            }

            .link:hover {
              border-bottom: 0px;
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
