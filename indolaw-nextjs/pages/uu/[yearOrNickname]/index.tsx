import fs from "fs";
import { GetStaticProps } from "next";
import { Complex } from "utils/grammar";
import LawPage from "components/LawPage";
import { LAW_NICKNAMES } from "utils/law-nicknames";

export default function Nickname(props: {
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
    paths: Object.keys(LAW_NICKNAMES).map(nickname => ({
      params: {
        yearOrNickname: nickname,
      }
    })),
    fallback: false,
  }
}

export const getStaticProps: GetStaticProps = async ({ params }) => {
  if (params == null ||
    typeof params.yearOrNickname !== 'string' ||
    !(params.yearOrNickname in LAW_NICKNAMES)
  ) {
    return { notFound: true };
  }

  const id = LAW_NICKNAMES[params.yearOrNickname];
  const file = fs.readFileSync(`./laws/${id}.json`, 'utf8');

  // e.g 'uu-2003-13'
  const [_, year, number] = id.split('-')

  return {
    props: {
      data: {
        law: JSON.parse(file),
        year,
        number,
      },
    },
  };
};
