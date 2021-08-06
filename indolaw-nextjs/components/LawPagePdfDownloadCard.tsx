import { Metadata } from "utils/grammar";
import StyledLink from "./StyledLink";
import { fonts } from "utils/theme";
import LawPageCard from "./LawPageCard";
import { useAppContext } from "utils/context-provider";

export default function LawPagePdfDownloadCard(props: {
  lawNameAndYear: string,
  pdfLink: string,
  webpageLink: string,
}): JSX.Element {
  const { lawNameAndYear, pdfLink, webpageLink } = props;
  const { colorScheme } = useAppContext();

  return (
    <>
      <style jsx>{`
        .container {
          font-family: ${fonts.serif};
          font-size: 18px;
          color: ${colorScheme.text};
          padding: 4px 0;
        }

        .explainer {
          margin-bottom: 20px;
        }

        .download {
          margin-bottom: 8px;
        }
      `}</style>
      <LawPageCard>
        <div className="container">
          <p className="explainer">
            🚧 Maaf, undang-undang ini masih belum tersedia dalam format web. Download PDF {lawNameAndYear} dari situs resmi <em><b>peraturan.bpk.go.id</b></em> lewat link dibawah.
          </p>
          <p className="download">
            <StyledLink
              text={'Download PDF dari peraturan.bpk.go.id'}
              link={pdfLink}
              iconName={'description'}
            />
          </p>
          <p>
            <StyledLink
              text={'Lihat halaman resmi di peraturan.bpk.go.id'}
              link={webpageLink}
              iconName={'open_in_new'}
            />
          </p>
        </div>
      </LawPageCard>
    </>
  );
}