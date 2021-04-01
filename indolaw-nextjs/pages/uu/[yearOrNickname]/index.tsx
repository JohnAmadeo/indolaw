import fs from "fs";
import { GetStaticProps } from "next";
import { LawData } from "utils/grammar";
import LawPage from "components/LawPage";
import { LAW_NICKNAMES } from "utils/law-nicknames";

export default function Nickname(props: {
  data: {
    law: LawData;
  };
}): JSX.Element {
  return (
    <LawPage
      law={props.data.law}
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

  return {
    props: {
      data: {
        law: JSON.parse(file),
      },
    },
  };
};
