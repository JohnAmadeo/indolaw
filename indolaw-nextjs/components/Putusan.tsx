import { LawData } from "utils/grammar";
import TrayButton from "./TrayButton";

export default function Putusan(props: {
  law: LawData,
  textColor: string,
}): JSX.Element {
  const { law: { metadata } } = props;

  return (
    <TrayButton
      onClick={() => {
        // TODO(johnamadeo): Add a text box so users can enter their own keywords
        let topicKeywords;
        if (metadata.topic.length <= 30) {
          topicKeywords = metadata.topic;
        } else {
          topicKeywords = `Undang-Undang Nomor ${metadata.number} Tahun ${metadata.year}`;
        }
        topicKeywords = topicKeywords.split(' ').join('+');

        const maUrl = `https://putusan3.mahkamahagung.go.id/search.html?q=${topicKeywords}`;
        const mkUrl = `https://www.mkri.id/index.php?page=web.Putusan&id=1&kat=5&cari=${topicKeywords}`;
        window.open(mkUrl, '_blank');
        window.open(maUrl, '_blank');
      }}
      iconName={'open_in_new'}
      text={'Lihat Putusan Terkait'}
    />
  );
}