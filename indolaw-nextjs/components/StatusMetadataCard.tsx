import { Metadata } from "utils/grammar";
import { useAppContext } from "../utils/context-provider";
import MetadataCard from "./MetadataCard";

export default function StatusMetadataCard(props: {
  metadata: Metadata;
}): JSX.Element {
  const status = props.metadata['status'];
  const capitalizeFirstLetter = (str: string) => str[0].toUpperCase() + str.slice(1);
  const headings = Object.keys(status);

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

        .none {
          margin: 16px;
        }
      `}</style>
      <MetadataCard
        title={'Status'}
        body={headings.length > 0 ? (
          <ul>
            {headings.map(heading => (
              <li>
                <p>{capitalizeFirstLetter(heading)}</p>
                <ul>
                  {status[heading].map(e => (
                    <li>
                      <a href={e.link} target="_blank">{e.law}</a>
                    </li>
                  ))}
                </ul>
              </li>
            ))}
          </ul>
        ) : (
          <div className="none">N/A</div>
        )}
      />
    </>
  );
}