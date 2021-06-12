import { Complex, Primitive, renderChildren, Structure } from "utils/grammar";
import { fonts } from "utils/theme";

// TODO(johnamadeo): Fix "Warning: Each child in a list should have a unique "key" prop." problem
export default function Law(props: { law: Complex, colorScheme : any}): JSX.Element {
  const penjelasanUmum = extractPenjelasanUmum(props.law);

  return (
    <div>
      <style jsx>{`
        div {
          font-family: ${fonts.serif};
          font-size: 18px;
          color: ${props.colorScheme.text};
        }
      `}</style>
      {renderChildren(props.law, undefined, penjelasanUmum)}
    </div>
  );
}

function extractPenjelasanUmum(lawNode: Complex): Array<Primitive | Complex> {
  if (lawNode.children) {
    const penjelasanUmum = lawNode.children[lawNode.children.length - 1];

    if (penjelasanUmum.type.match(Structure.PENJELASAN) && (penjelasanUmum as Complex).children) {
      const penjelasanPasalDemiPasal = (penjelasanUmum as Complex).children[(penjelasanUmum as Complex).children.length - 1];

      if (penjelasanPasalDemiPasal.type.match(Structure.PENJELASAN_PASAL_DEMI_PASAL)) {
        // remove the first node in the list of nodes (only contains the title of Penjelasan Umum)
        return (penjelasanPasalDemiPasal as Complex).children.slice(1);
      }
    }
  }

  return [];
}
