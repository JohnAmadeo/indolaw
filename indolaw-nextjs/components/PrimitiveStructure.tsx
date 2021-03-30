import { CSSProperties } from "react";
import { Primitive, Structure } from "utils/grammar";
import { colors } from "utils/theme";
import Link from "next/link";

export default function PrimitiveStructure(props: {
  structure: Primitive;
  customStyle?: CSSProperties;
}): JSX.Element {
  const { structure: { text, type }, customStyle } = props;

  return (
    <div style={{ ...customStyle }}>
      {/* 
        TODO(johnamadeo: Figure out how to fix the styling hack below.
        
        Ideally we want consistent margins, but the problem is that 4px
        top/bottom margins look great on everything other than consecutive
        plaintext bloks with lots of words (mostly in Penjelasan)
      */}
      <style jsx>{`
        div {
          margin: 4px 0 ${text.length > 350 ? 16 : 4}px 0;
          font-size: 18px;
        }
      `}</style>
      <p>{text}</p>
      {/* <p>{type === Structure.PLAINTEXT ? maybeLinkToOtherLaws(text) : text}</p> */}
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

  let linkedSpans = [];
  for (let i = 0; i < spans.length; i++) {
    const isLinkable = spans[i].match(regex) != null;
    if (isLinkable) {
      linkedSpans.push(
        <span className="link">
          <style jsx>{`
            .link {
              color: ${colors.background};
            }

            .link:hover {
              text-decoration: underline;
            }
          `}</style>
          <a
            key={i}
            target="_blank"
            rel="noopener noreferrer"
            href={'https://search.hukumonline.com/search/all/?q=undang+undang+13+2003&language=%5B%22id%22%5D'}
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