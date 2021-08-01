import { useAppContext } from "utils/context-provider";
import { Metadata } from "utils/grammar";
import MetadataCard from "./MetadataCard";
import StyledLink from "./StyledLink";

export default function PengujianUndangUndangMetadataCard(props: {
  metadata: Metadata;
}): JSX.Element {
  const puu = props.metadata['puu'];
  const { colorScheme } = useAppContext();

  return (
    <>
      <style jsx >{`
        li {
          margin: 8px 0;
        }

        span {
          color: ${colorScheme.textHover};
        }

        .none {
          margin: 16px;
        }

        .name {
          margin-bottom: 4px;
        }
      `}</style>
      <MetadataCard
        title={'Uji Materi Mahkamah Konstitusi'}
        body={puu.length > 0 ? (
          <ul>
            {puu.map(e => (
              <li>
                <p className="name">
                  <StyledLink text={e.id} link={e.link} />
                </p>
                <p><span>{e.context}</span></p>
              </li>
            ))}
          </ul>
        ) : <p className="none">N/A</p>}
      />
    </>
  );
}