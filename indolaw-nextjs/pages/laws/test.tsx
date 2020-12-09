import remark from "remark";
import html from "remark-html";
import matter from "gray-matter";
import fs from "fs";
import path from "path";
import { GetStaticProps } from "next";
import { CSSProperties } from "react";

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

const HEADING_STRUCTURES = new Set([
  Structure.BAB_NUMBER,
  Structure.BAB_TITLE,
  Structure.PASAL_NUMBER,
  Structure.BAGIAN_NUMBER,
  Structure.BAGIAN_TITLE,
  Structure.PARAGRAF_NUMBER,
  Structure.PARAGRAF_TITLE,
]);

interface PrimitiveStructure {
  type: string;
  type: Structure;
  text: string;
}

interface ComplexStructure {
  type: Structure;
  children: Array<PrimitiveStructure | ComplexStructure>;
}

export default function Test(props: {
  data: {
    law: any;
  };
}) {
  return (
    <div style={{ margin: "0 180px" }}>
      <h1>UNDANG UNDANG REPUBLIK INDONESIA TENTANG CIPTA KERJA</h1>
      {renderStructure(props.data.law, 1)}
    </div>
  );
}

function renderStructure(structure: any, depth: number) {
  return (
    <>
      {structure.map((childStructure: any) => {
        if (childStructure instanceof Array) {
          return renderStructure(childStructure, depth + 1);
        } else {
          return renderPrimitive(childStructure, depth);
        }
      })}
    </>
  );
}

function renderPrimitive(structure: PrimitiveStructure, depth: number) {
  let divStyle: CSSProperties = {
    marginLeft: `${depth * 32}px`,
    marginBottom: "12px",
    fontSize: "20px",
    border: "1px solid red",
  };
  let textStyle: CSSProperties = {};

  if (HEADING_STRUCTURES.has(Structure[structure.type])) {
    textStyle.fontWeight = "bold";
    divStyle.marginLeft = "0px";
    divStyle.textAlign = "center";
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
