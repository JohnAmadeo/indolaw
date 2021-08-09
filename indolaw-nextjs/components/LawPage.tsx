import { LawData } from "utils/grammar";
import Head from "next/head";
import dynamic from 'next/dynamic'

import DesktopLawPage from "./DesktopLawPage";
import MobileLawPage from "./MobileLawPage";
import { useEffect, useRef, useState } from "react";

// TODO(johnamadeo): Fix "Warning: Each child in a list should have a unique "key" prop." problem
export default function LawPage(props: { law: LawData }): JSX.Element {
  const { law } = props;

  const [isMobileDevice, setIsMobileDevice] = useState(false);

  useEffect(() => {
    async function detectDevice() {
      const { isMobile } = await import('react-device-detect');
      setIsMobileDevice(isMobile);
    }

    detectDevice();
  }, [setIsMobileDevice]);

  return (
    <div>
      <Head>
        <title>UU No. {law.metadata.number} Tahun {law.metadata.year}</title>
        <meta name="viewport" content="initial-scale=1.0, width=device-width" />
      </Head>
      <h1>{isMobileDevice ? 'isMobile' : 'NOT isMobile'}</h1>
      {isMobileDevice ? <MobileLawPage law={law} /> : <DesktopLawPage law={law} />}
    </div>
  );
}
