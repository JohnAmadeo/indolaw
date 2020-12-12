import fs from "fs";
import { GetStaticProps } from "next";
import { Complex } from "utils/grammar";
import Law from "components/Law";
import React from "react";
import TableOfContentsGroup from "components/TableOfContentsGroup";
import { colors } from "utils/theme";

// TODO(johnamadeo): Fix "Warning: Each child in a list should have a unique "key" prop." problem
export default function Test(props: {
  data: {
    law: Complex;
  };
}): JSX.Element {
  const border = "1px solid blue";
  const navWidth = "400px";

  return (
    <div>
      <div
        style={{
          // border: border,
          height: "100%",
          overflow: "scroll",
          position: "fixed",
          padding: "12px",
          width: navWidth,
          backgroundColor: colors.background,
        }}
      >
        {props.data.law.children.map((child) => (
          <TableOfContentsGroup structure={child} depth={0} />
        ))}
      </div>

      <div
        style={{
          // border: border,
          position: "absolute",
          left: navWidth,
          right: 0,
        }}
      >
        <div
          style={{
            // border: border,
            margin: "0 auto",
            width: "768px",
          }}
        >
          <Law law={props.data.law} />
        </div>
      </div>
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
