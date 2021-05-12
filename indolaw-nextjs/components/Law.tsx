import { Complex, Metadata, renderChildren } from "utils/grammar";
import { fonts } from "utils/theme";
import Tooltip from "./Tooltip";

// TODO(johnamadeo): Fix "Warning: Each child in a list should have a unique "key" prop." problem
export default function Law(props: {
  metadata: Metadata;
  law: Complex;
  colorScheme: any;
}): JSX.Element {
  return (
    <div>
      <style jsx>{`
        div {
          font-family: ${fonts.serif};
          color: ${props.colorScheme.text};
        }
      `}</style>
      {renderChildren(props.law)}
      <Tooltip metadata={props.metadata}></Tooltip>
    </div>
  );
}
