import { Complex, Primitive, renderStructure } from "utils/grammar";

export default function PenjelasanPasalItem(props: {
  structure: Complex;
  numOfHeadingLines: number;
}): JSX.Element {
  const { structure, numOfHeadingLines } = props;

  return (
    <>
      <style jsx>{`
        div {
          font-size: 15px;
          margin: 20px auto;
          width: 90%;
          background-color: grey;
          color: #F0FFF0;
          padding: 20px;
          border-radius: 7.5px;
        }

        p {
            font-size: 16px;
          margin: 8px 0;
          font-weight: 700;
          text-align: center;
          line-height: 1.5;
        }
      `}</style>
      <div> <p> Penjelasan </p>{structure.children
            .slice(numOfHeadingLines)
            .map((child, idx) => {
                if ((child as Primitive).text && (child as Primitive).text.startsWith('TAMBAHAN LEMBARAN NEGARA REPUBLIK INDONESIA')) {
                    return <></>;
                }

                return renderStructure(child, idx);
            })}
      </div>
    </>
  );
}
