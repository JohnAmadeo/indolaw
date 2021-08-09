import { LawData } from "utils/grammar";
import Head from "next/head";
import { isMobile } from 'react-device-detect';

import DesktopLawPage from "./DesktopLawPage";
import MobileLawPage from "./MobileLawPage";

// TODO(johnamadeo): Fix "Warning: Each child in a list should have a unique "key" prop." problem
export default function LawPage(props: { law: LawData }): JSX.Element {
  const { law } = props;

  return (
    <div>
      <Head>
        <title>UU No. {law.metadata.number} Tahun {law.metadata.year}</title>
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      </Head>
      {isMobile ? <MobileLawPage law={law} /> : <DesktopLawPage law={law} />}
    </div>
  );
}
