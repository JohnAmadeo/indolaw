import { LawData } from "utils/grammar";
import TrayButton from "./TrayButton";

export default function PutusanMK(props: { law: LawData }): JSX.Element {
  const { law: { metadata } } = props;

  return (
    <TrayButton
      onClick={() => {
        // TODO(johnamadeo): Unclear how well this works for UU Perubahan
        let topicKeywords;
        if (metadata.topic.length <= 30) {
          topicKeywords = metadata.topic;
        } else {
          topicKeywords = `Undang-Undang Nomor ${metadata.number} Tahun ${metadata.year}`;
        }
        topicKeywords = topicKeywords.split(' ').join('+');

        const mkUrl = `https://www.mkri.id/index.php?page=web.Putusan&id=1&kat=5&cari=${topicKeywords}`;
        window.open(mkUrl, '_blank');
      }}
      iconName={'open_in_new'}
      text={'Lihat Putusan MK Terkait'}
    />
  );
}