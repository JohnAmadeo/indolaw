import { Metadata } from "utils/grammar";
import LawPageMetadataSection from "./LawPageMetadataSection";
import StyledLink from "./StyledLink";
import _ from "lodash";
import LawPageCard from "./LawPageCard";

export default function LawPageMetadataCard(props: {
  metadata: Metadata,
}): JSX.Element {
  const { status, puu, theme } = props.metadata;
  const headings = Object.keys(status);

  return (
    <LawPageCard>
      <>
        {headings.map(heading => (
          <LawPageMetadataSection
            key={heading}
            title={_.capitalize(heading)}
            list={status[heading].map(e => <StyledLink text={e.law} link={e.link} />)}
            isLast={false}
          />
        ))}
        {puu.length > 0 && (
          <LawPageMetadataSection
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
          <LawPageMetadataSection
            title={'Tema'}
            list={theme.map(e => (
              <StyledLink text={e.theme} link={e.link} />
            ))}
            isLast
          />
        )}
      </>
    </LawPageCard>
  );
}