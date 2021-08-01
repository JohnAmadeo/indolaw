import { Metadata } from "utils/grammar";
import ThemeMetadataCard from "./ThemeMetadataCard";
import StatusMetadataCard from "./StatusMetadataCard";
import PengujianUndangUndangMetadataCard from "./PengujianUndangUndangMetadataCard";
import { fonts } from "utils/theme";
import { useAppContext } from "utils/context-provider";
import Divider from "./Divider";

export default function MetadataCardsSection(props: {
  metadata: Metadata;
}): JSX.Element {
  const { metadata } = props;
  const { year, number, topic } = metadata;
  const { colorScheme } = useAppContext();

  const nameAndYear = `UU No. ${number} Tahun ${year}`;
  const topicText = `Tentang ${topic}`;
  return (
    <div>
      <style jsx>{`
        .name-and-year {
          margin: 12px 0 0 0;
          font-family: ${fonts.serif};
          font-size: 48px;
          color: ${colorScheme.text};
        }

        .topic {
          margin: 0 0 12px 0;
          font-family: ${fonts.serif};
          font-size: ${topicText.length > 60 ? '26px' : '48px'};
          color: ${colorScheme.text};
        }

        .card {
          margin: 24px 0;
        }
      `}</style>
      <h1 className="name-and-year">{nameAndYear}</h1>
      <h1 className="topic">{topicText}</h1>
      <div className="card">
        <ThemeMetadataCard metadata={metadata} />
      </div>
      <div className="card">
        <StatusMetadataCard metadata={metadata} />
      </div>
      <div className="card">
        <PengujianUndangUndangMetadataCard metadata={metadata} />
      </div>
      <Divider />
    </div>
  );
}