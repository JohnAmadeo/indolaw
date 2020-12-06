import remark from "remark";
import html from "remark-html";
import matter from "gray-matter";
import fs from "fs";
import path from "path";
import { GetStaticProps } from "next";
enum Structure {
  UNDANG_UNDANG = "UNDANG_UNDANG",
  BAB = "BAB",
  BAB_NUMBER = "BAB_NUMBER",
  BAB_TITLE = "BAB_TITLE",
  PASAL = "PASAL",
  PASAL_NUMBER = "PASAL_NUMBER",
  BAGIAN = "BAGIAN",
  BAGIAN_TITLE = "BAGIAN_TITLE",
  BAGIAN_NUMBER = "BAGIAN_NUMBER",
  PARAGRAF = "PARAGRAF",
  PARAGRAF_TITLE = "PARAGRAF_TITLE",
  PARAGRAF_NUMBER = "PARAGRAF_NUMBER",
  PLAINTEXT = "PLAINTEXT",
  LIST = "LIST",
  LIST_ITEM = "LIST_ITEM",
  LIST_INDEX = "LIST_INDEX",
  NUMBER_WITH_BRACKETS = "NUMBER_WITH_BRACKETS",
  NUMBER_WITH_DOT = "NUMBER_WITH_DOT",
  LETTER_WITH_DOT = "LETTER_WITH_DOT",
}


export default function Test(props: {
  data: {
    law: any;
  };
}) {
  return (
    <div style={{ margin: "0 124px" }}>
      <h1>UNDANG UNDANG REPUBLIK INDONESIA TENTANG CIPTA KERJA</h1>
      {render(props.data.law, 1)}
    </div>
  );
}

function render(structure: any, depth: number) {
  return (
    <>
      {structure.map((childStructure: any) => {
        if (childStructure instanceof Array) {
          return render(childStructure, depth + 1);
        } else {
          return renderPrimitive(childStructure, depth);
        }
      })}
    </>
  );
}

function renderPrimitive(structure: any, depth: number) {
  const divStyle = {
    marginLeft: `${depth * 32}px`,
    marginBottom: "12px",
    fontSize: "20px",
  };

  let textStyle = {};
  if (
    structure.type.toLowerCase().includes("number") ||
    structure.type.toLowerCase().includes("title")
  ) {
    textStyle = { fontWeight: "bold" };
  }

  return (
    <div style={divStyle}>
      <p style={textStyle}>{structure.text}</p>
    </div>
  );
}

export const getStaticProps: GetStaticProps = async () => {
  const filePath = "../indolaw-parser/omnibus_law_pg_3_13.json";
  const file = fs.readFileSync(filePath, "utf8");

  return {
    props: {
      data: {
        law: JSON.parse(file),
      },
    },
  };
};
