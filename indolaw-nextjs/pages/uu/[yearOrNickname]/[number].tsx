import fs from "fs";
import { GetStaticProps } from "next";
import { Complex } from "utils/grammar";
import LawPage from "components/LawPage";

export default function Number(props: {
  data: {
    law: Complex;
    year: number;
    number: number;
  };
}): JSX.Element {
  return (
    <LawPage
      law={props.data.law}
      year={props.data.year}
      number={props.data.number}
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

  const file = fs.readFileSync(`./laws/uu-${params.yearOrNickname}-${params.number}.json`, 'utf8');

  return {
    props: {
      data: {
        law: JSON.parse(file)['content'],
        year: params.yearOrNickname,
        number: params.number,
      },
    },
  };
};
