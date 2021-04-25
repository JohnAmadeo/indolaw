import { useState } from "react";
import { Metadata } from "utils/grammar";
import { fonts } from "utils/theme";
import TrayButton from "./TrayButton";
import ReactDOMServer from "react-dom/server";
import * as clipboard from "clipboard-polyfill";

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

  const [buttonText, setButtonText] = useState('Click to Copy');
  const [iconName, setIconName] = useState('content_copy');

  const citationText = (
    <span>
      <span style={{ fontStyle: 'italic' }}>
        Undang-Undang Tentang {topic},
        UU Nomor {number} Tahun {year},
      </span>
      {' '}
      Lembaran Negara Nomor {lembaranNegaraNumber} Tahun {lembaranNegaraYear},
      Tambahan Lembaran Negara Nomor {tambahanLembaranNumber}
    </span>
  );

  const htmlToCopy = ReactDOMServer.renderToStaticMarkup(citationText);

  return (
    <div>
      <style jsx>{`
        div.container {
          color: ${props.textColor};
          font-family: ${fonts.sans};
          font-size: 14px;
        }

        span {
          font-style: italic;
        }

        div.copy {
          margin-top: 12px;
        }
      `}</style>
      <div className="container" id="copytarget">
        {citationText}
      </div>
      <div className="copy">
        <TrayButton
          iconName={iconName}
          text={buttonText}
          onClick={async () => {
            const item = new clipboard.ClipboardItem({
              "text/html": new Blob(
                [htmlToCopy],
                { type: "text/html" }
              )
            });
            await clipboard.write([item]);

            setButtonText('Copied!');
            setIconName('check');

            setTimeout(() => {
              setButtonText('Click to Copy');
              setIconName('content_copy');
            }, 2000);
          }}
        />
      </div>
    </div>
  );
}
