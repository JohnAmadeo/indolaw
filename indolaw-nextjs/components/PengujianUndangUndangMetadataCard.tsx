import { useAppContext } from "utils/context-provider";
import { Metadata } from "utils/grammar";
import MetadataCard from "./MetadataCard";

export default function PengujianUndangUndangMetadataCard(props: {
  metadata: Metadata;
}): JSX.Element {
  const puu = props.metadata['puu'];
  const { colorScheme } = useAppContext();

  return (
    <>
      <style jsx >{`
        a:hover {
          color: ${colorScheme.textHover};
        }

        li {
          margin: 8px 0;
        }

        span {
          color: ${colorScheme.textHover};
        }

        .none {
          margin: 16px;
        }
      `}</style>
      <MetadataCard
        title={'Uji Materi Mahkamah Konstitusi'}
        body={puu.length > 0 ? (
          <ul>
            {puu.map(e => (
              <li>
                <p>
                  <a href={e.link} target="_blank">
                    {e.id}
                  </a>
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