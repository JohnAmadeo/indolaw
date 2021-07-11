import fs from "fs";
import { GetStaticProps } from "next";
import { LawData } from "utils/grammar";
import LawPage from "components/LawPage";
import { getDirectoryMetadata } from "utils/route-utils";

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
  return {
    paths: fs.readdirSync('./laws')
      .map(filename => {
        const parts = filename.replace(/\.json$/, '').split('-');
        return {
          params: {
            yearOrNickname: parts[1], // year
            number: parts[2],
          },
        };
      }),
    fallback: false,
  }
}

export const getStaticProps: GetStaticProps = async ({ params }) => {
  if (params == null) {
    return { notFound: true };
  }

  const year = params.yearOrNickname as string;
  const number = params.number as string;

  const law = JSON.parse(fs.readFileSync(`./laws/uu-${year}-${number}.json`, 'utf8'));
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
