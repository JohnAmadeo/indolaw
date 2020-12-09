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

const PRIMITIVE_STRUCTURES = new Set([
  Structure.PLAINTEXT,
  Structure.BAB_NUMBER,
  Structure.BAB_TITLE,
  Structure.PASAL_NUMBER,
  Structure.BAGIAN_NUMBER,
  Structure.BAGIAN_TITLE,
  Structure.PARAGRAF_NUMBER,
  Structure.PARAGRAF_TITLE,
]);

interface Primitive {
  type: Structure;
  text: string;
}

interface Complex {
  type: Structure;
  children: Array<Primitive | Complex>;
}

export default function Test(props: {
  data: {
    law: Complex;
  };
}) {
  return (
    <div
      style={{
        width: "800px",
        margin: "0 auto",
      }}
    >
      <h1>UNDANG UNDANG REPUBLIK INDONESIA TENTANG CIPTA KERJA</h1>
      {renderUndangUndang(props.data.law)}
    </div>
  );
}

function renderStructure(structure: Complex | Primitive) {
  switch (structure.type) {
    case Structure.PLAINTEXT:
    case Structure.BAB_NUMBER:
    case Structure.BAB_TITLE:
    case Structure.PASAL_NUMBER:
    case Structure.BAGIAN_NUMBER:
    case Structure.BAGIAN_TITLE:
    case Structure.PARAGRAF_NUMBER:
    case Structure.PARAGRAF_TITLE:
      return renderPrimitive(structure as Primitive);
    case Structure.BAB:
    case Structure.BAGIAN:
    case Structure.PARAGRAF:
      return renderStructuresWithTitleAndNumber(structure as Complex);
    case Structure.LIST:
      return renderList(structure as Complex);
    case Structure.LIST_ITEM:
      return renderListItem(structure as Complex);
    case Structure.PASAL:
      return renderPasal(structure as Complex);
    default:
      return <></>;
  }
}

function renderPrimitive(
  structure: Primitive,
  customStyle: CSSProperties = {}
): JSX.Element {
  let style: CSSProperties = {
    margin: "4px 0",
    fontSize: "20px",
    // border: "1px solid red",
  };

  return (
    <div style={{ ...style, ...customStyle }}>
      <p>{structure.text}</p>
    </div>
  );
}

// TODO(johnamadeo): I think there are multi-line titles later on in the text
function renderStructuresWithTitleAndNumber(structure: Complex): JSX.Element {
  const style: CSSProperties = {
    margin: "48px 0",
  };

  const headingStyle: CSSProperties = {
    marginLeft: "0px",
    textAlign: "center",
    margin: "8px 0",
  };

  return (
    <>
      <div style={style}>
        {renderPrimitive(structure.children[0] as Primitive, headingStyle)}
        {renderPrimitive(structure.children[1] as Primitive, headingStyle)}
      </div>
      {structure.children
        .slice(2)
        .map((childStructure) => renderStructure(childStructure))}
    </>
  );
}

function renderList(structure: Complex): JSX.Element {
  return (
    <div>
      {structure.children.map((childStructure) =>
        renderStructure(childStructure)
      )}
    </div>
  );
}

function renderListItem(structure: Complex): JSX.Element {
  // TODO(johnamadeo): Decide how the heck we wanna do CSS (CSS modules, big CSS object at bottom?)
  return (
    <div
      style={{
        display: "flex",
        margin: "4px 0",
      }}
    >
      <div
        style={{
          minWidth: "48px",
        }}
      >
        {renderPrimitive(structure.children[0] as Primitive)}
      </div>
      <div
        style={{
          flexGrow: 1,
        }}
      >
        {structure.children.map((childStructure) => {
          if (childStructure.type === Structure.PLAINTEXT) {
            return renderPrimitive(childStructure as Primitive, {
              textAlign: "justify",
            });
          }

          return renderStructure(childStructure);
        })}
      </div>
    </div>
  );
}

function renderPasal(structure: Complex): JSX.Element {
  const style: CSSProperties = {
    margin: "48px 0 0 0",
  };
  const headingStyle: CSSProperties = {
    marginLeft: "0px",
    textAlign: "center",
    margin: "8px 0",
  };
  return (
    <>
      <div style={style}>
        {renderPrimitive(structure.children[0] as Primitive, headingStyle)}
      </div>
      {structure.children
        .slice(1)
        .map((childStructure) => renderStructure(childStructure))}
    </>
  );
}

function renderUndangUndang(structure: Complex): JSX.Element {
  return <>{structure.children.map((children) => renderStructure(children))}</>;
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
