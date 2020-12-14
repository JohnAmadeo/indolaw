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
      <div className="table-of-contents-container">
        <style jsx>{`
          .table-of-contents-container {
            height: 100%;
            overflow: scroll;
            position: fixed;
            padding: 20px 12px;
            width: ${navWidth};
            background-color: ${colors.background};
          }
        `}</style>
        {props.data.law.children.map((child) => (
          <TableOfContentsGroup structure={child} depth={0} />
        ))}
      </div>

      <div className="law-container">
        <style jsx>{`
          .law-container {
            position: absolute;
            left: ${navWidth};
            right: 0;
          }

          .law {
            margin: 0 auto;
            width: 768px;
          }
        `}</style>
        <div className="law">
          <Law law={props.data.law} />
        </div>
      </div>
    </div>
  );
}

export const getStaticProps: GetStaticProps = async () => {
  const filePath = "../indolaw-parser/omnibus_law_pg_3_13_modified.json";
  const file = fs.readFileSync(filePath, "utf8");

  return {
    props: {
      data: {
        law: JSON.parse(file),
      },
    },
  };
};
