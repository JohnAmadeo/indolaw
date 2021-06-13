import { useMemo } from "react";
import { Complex, Primitive, renderChildren, Structure, NodeMap } from "utils/grammar";
import { fonts } from "utils/theme";
import { LawContext, getPenjelasanMapKey } from "utils/context-provider";

// TODO(johnamadeo): Fix "Warning: Each child in a list should have a unique "key" prop." problem
export default function Law(props: { law: Complex, colorScheme: any }): JSX.Element {
  // This method requires a brute force traversal of PENJELASAN_PASAL_DEMI_PASAL
  // so we want to run it once & memoize
  const penjelasanMap = useMemo(() => extractPenjelasanMap(props.law), [props.law]);
  console.log(penjelasanMap);

  return (
    <LawContext.Provider value={{ penjelasanMap }}>
      <div>
        <style jsx>{`
        div {
          font-family: ${fonts.serif};
          font-size: 18px;
          color: ${props.colorScheme.text};
        }
      `}</style>
        {renderChildren(props.law, undefined)}
      </div>
    </LawContext.Provider>
  );
}

function extractPenjelasanMap(law: Complex): NodeMap {
  const penjelasan = (law.children[law.children.length - 1] as Complex);
  const penjelasanPasalDemiPasal = penjelasan.children[penjelasan.children.length - 1];
  const penjelasanMap: NodeMap = {};

  function traverse(node: Complex | Primitive) {
    if (node.children !== undefined) {

      node = node as Complex;
      if (node.type === Structure.PASAL || node.type == Structure.MODIFIED_PASAL) {
        const pasalNumber = node.children[0] as Primitive;
        const key = getPenjelasanMapKey(node.type, pasalNumber.text);
        penjelasanMap[key] = node;
      }

      for (let child of node.children) {
        traverse(child);
      }
    }
  }

  traverse(penjelasanPasalDemiPasal);
  return penjelasanMap;
}
