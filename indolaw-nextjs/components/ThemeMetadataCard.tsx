import { Metadata } from "utils/grammar";
import { useAppContext } from "../utils/context-provider";
import MetadataCard from "./MetadataCard";
import StyledLink from "./StyledLink";

export default function ThemeMetadataCard(props: {
  metadata: Metadata;
}): JSX.Element {
  const theme = props.metadata['theme'];

  return (
    <>
      <style jsx >{`
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
                <StyledLink text={e.theme} link={e.link} />
              </li>
            ))}
          </ul>
        )}
      />
    </>
  );
}