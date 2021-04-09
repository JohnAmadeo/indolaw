import { CSSProperties } from "react";
import { Metadata } from "utils/grammar";
import { colors, fonts } from "utils/theme";

export default function Citation(props: {
  metadata: Metadata,
  textColor: string,
}): JSX.Element {
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
          color: ${props.textColor};
          font-family: ${fonts.sans};
          font-size: 14px;
        }

        span {
          font-style: italic;
        }
      `}</style>
      <span>
        Undang-Undang Tentang {topic},
        UU Nomor {number} Tahun {year},
      </span>
      {' '}
      Lembaran Negara Nomor {lembaranNegaraNumber} Tahun {lembaranNegaraYear},
      Tambahan Lembaran Negara Nomor {tambahanLembaranNumber}
    </div>
  );
}
