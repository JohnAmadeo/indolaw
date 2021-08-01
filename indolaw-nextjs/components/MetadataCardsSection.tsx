import { Metadata } from "utils/grammar";
import { useAppContext } from "../utils/context-provider";
import MetadataCard from "./MetadataCard";
import StyledLink from "./StyledLink";

export default function MetadataCardsSection(props: {
  metadata: Metadata,
}): JSX.Element {
  const { status, puu, theme } = props.metadata;
  const { colorScheme } = useAppContext();

  const capitalizeFirstLetter = (str: string) => str[0].toUpperCase() + str.slice(1);
  const headings = Object.keys(status);

  return (
    <div className="container">
      <style jsx >{`
        .container {
          border: 1px solid ${colorScheme.clickable};
          padding: 36px;
          border-radius: 8px;
        }

        li {
          margin: 8px 0;
        }

        .none {
          margin: 16px;
        }

        span {
          color: ${colorScheme.textHover};
        }
      `}</style>
      {headings.map(heading => (
        <MetadataCard
          title={capitalizeFirstLetter(heading)}
          list={status[heading].map(e => <StyledLink text={e.law} link={e.link} />)}
          isLast={false}
        />
      ))}
      {puu.length > 0 && (
        <MetadataCard
          title={'Uji Materi Mahkamah Konstitusi'}
          list={puu.map(e => (
            <>
              <p className="name">
                <StyledLink text={e.id} link={e.link} />
              </p>
              <p><span>{e.context}</span></p>
            </>
          ))}
          isLast={false}
        />
      )}
      {theme.length > 0 && (
        <MetadataCard
          title={'Tema'}
          list={theme.map(e => (
            <StyledLink text={e.theme} link={e.link} />
          ))}
          isLast
        />
      )}
    </div>
  );
}