import fs from "fs";
import { GetStaticProps } from "next";
import { Complex } from "utils/grammar";
import TableOfContents from "components/TableOfContents";
import Law from "components/Law";

// TODO(johnamadeo): Fix "Warning: Each child in a list should have a unique "key" prop." problem
export default function Test(props: {
  data: {
    law: Complex;
  };
}): JSX.Element {
  const border = "1px solid blue";
  const navWidth = "400px";
  return (
    <div style={{ border: border }}>
      <div
        style={{
          border: border,
          height: "100%",
          overflow: "scroll",
          position: "fixed",
          padding: "12px",
          width: navWidth,
        }}
      >
        <div
          style={{
            border: border,
            padding: "8px",
          }}
        >
          Header / Go to Home
        </div>
        <TableOfContents law={props.data.law} />
      </div>

      <div
        style={{
          border: border,
          position: "absolute",
          left: navWidth,
          right: 0,
        }}
      >
        <div
          style={{
            // border: border,
            margin: "0 auto",
            width: "800px",
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
