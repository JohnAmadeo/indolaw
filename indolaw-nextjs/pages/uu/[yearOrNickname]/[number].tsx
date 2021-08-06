import fs from "fs";
import { GetStaticPaths, GetStaticProps } from "next";
import { LawData } from "utils/grammar";
import LawPage from "components/LawPage";
import { getDirectoryMetadata, getLawPaths } from "utils/route-utils";

export default function Number(props: {
  data: {
    law: LawData
  }
}): JSX.Element {
  return (
    <LawPage
      law={props.data.law}
    />
  );
}

export async function getStaticPaths() {
  const p = getLawPaths();
  console.log(p);
  return {
    paths: p,
    fallback: false,
  }
}

export const getStaticProps: GetStaticProps = async ({ params }) => {
  if (params == null) {
    return { notFound: true };
  }

  const year = params.yearOrNickname as string;
  const number = params.number as string;

  const uuFilePath = `./laws/uu-${year}-${number}.json`;

  const law = fs.existsSync(uuFilePath)
    ? JSON.parse(fs.readFileSync(uuFilePath, 'utf8'))
    : {};

  const metadata = getDirectoryMetadata(year, number);

  law['metadata'] = {
    ...law['metadata'],
    ...metadata,
  }

  return {
    props: {
      data: {
        law,
      },
    },
  };
};
