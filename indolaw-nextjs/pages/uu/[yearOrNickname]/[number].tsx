import fs from "fs";
import { GetStaticProps } from "next";
import { LawData } from "utils/grammar";
import LawPage from "components/LawPage";

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

  // TODO(johnamadeo): This is obviously ugly. Find a better way to combine metadata from law JSON to directory JSON
  const directory = JSON.parse(fs.readFileSync(`../indolaw-parser/metadata/directory.json`, 'utf8'));
  // @ts-ignore
  var metadata = directory[year].find(entry => entry['number'] === parseInt(number));


  law['metadata'] = {
    ...law['metadata'],
    ...metadata,
  }

  console.log(law);

  return {
    props: {
      data: {
        law,
      },
    },
  };
};
