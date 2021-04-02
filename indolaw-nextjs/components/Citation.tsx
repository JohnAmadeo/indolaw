import { Metadata } from "utils/grammar";
import { colors, fonts } from "utils/theme";

export default function Citation(props: { metadata: Metadata }): JSX.Element {
  const {
    lembaranNegaraNumber,
    lembaranNegaraYear,
    tambahanLembaranNumber,
    number,
    topic,
    year,
  } = props.metadata;

  return (
    <div>
      <style jsx>{`
        div {
          color: ${colors.tray.text};
          font-family: ${fonts.sans};
        }

        span {
          font-style: italic;
        }
      `}</style>
      <span>
        Undang-Undang Tentang {topic},
        UU No. {number} Tahun {year},
      </span>
      {' '}
      Lembaran Negara No. {lembaranNegaraNumber} Tahun {lembaranNegaraYear},
      Tambahan Lembaran Negara No. {tambahanLembaranNumber}
    </div>
  );
}
