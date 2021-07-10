import { Metadata } from "utils/grammar";
import { useAppContext } from "../utils/context-provider";
import MetadataCard from "./MetadataCard";

export default function ThemeMetadataCard(props: {
  metadata: Metadata;
}): JSX.Element {
  const theme = props.metadata['theme'];
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
      `}</style>
      <MetadataCard
        title={'Tema'}
        body={(
          <ul>
            {theme.map(e => (
              <li>
                <a href={e.link} target="_blank">
                  {e.theme}
                </a>
              </li>
            ))}
          </ul>
        )}
      />
    </>
  );
}