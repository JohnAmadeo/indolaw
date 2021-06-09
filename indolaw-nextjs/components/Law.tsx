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
  // The structure of penjelasan umum node should follow:
  // UNDANG_UNDANG -> PENJELASAN -> PENJELASAN_PASAL_DEMI_PASAL -> [Penjelasan title, penjelasan pasal 1, penjelasan pasal 2, ...]
  const parentStructures = new Set([
    Structure.UNDANG_UNDANG,
    Structure.PENJELASAN,
  ]);

  for (const childNode of lawNode.children) {
    if (parentStructures.has(childNode.type)) {
      return extractPenjelasanUmum(childNode as Complex);
    } else if (childNode.type.match(Structure.PENJELASAN_PASAL_DEMI_PASAL)) {
      // remove the first node in the list of nodes (only contains the title of Penjelasan Umum)
      return (childNode as Complex).children.slice(1);
    }
  }

  return [];
}
