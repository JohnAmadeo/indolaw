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

function maybeLinkToOtherLaws(text: string): string | Array<JSX.Element> {
  // Limit links only to other Undang Undang (for now)
  // Using '\s+' to check for whitespace instead of ' ' is done because of our parser
  // can't catch double whitespace errors. In the long term we would want to ensure
  // the parser works really well so the UI doesn't need to have logic for quirks like this
  const regex = /(Undang-Undang\s+Nomor\s+[0-9]+\s+Tahun\s+[0-9]+)/;
  const spans = text.split(regex);

  if (spans.length === 1) {
    return text;
  }

  const { colorScheme } = useAppContext();

  let linkedSpans = [];
  for (let i = 0; i < spans.length; i++) {
    const isLinkable = spans[i].match(regex) != null;
    if (isLinkable) {
      linkedSpans.push(
        <span className="link">
          <style jsx>{`
            .link {
              color: ${colorScheme.linkText};
            }

            .link:hover {
              text-decoration: underline;
            }
          `}</style>
          <a
            key={i}
            target="_blank"
            rel="noopener noreferrer"
            href={
              "https://search.hukumonline.com/search/all/?q=undang+undang+13+2003&language=%5B%22id%22%5D"
            }
          >
            {spans[i]}
          </a>
        </span>
      );
    } else {
      linkedSpans.push(<span key={i}>{spans[i]}</span>);
    }
  }

  return linkedSpans;
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
