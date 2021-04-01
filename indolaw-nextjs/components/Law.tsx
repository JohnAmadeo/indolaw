import { Complex, renderChildren } from "utils/grammar";
import { fonts } from "utils/theme";

// TODO(johnamadeo): Fix "Warning: Each child in a list should have a unique "key" prop." problem
export default function Law(props: { law: Complex, colorScheme : any}): JSX.Element {
  return (
    <div>
      <style jsx>{`
        div {
          font-family: ${fonts.serif};
          color: ${props.colorScheme.text};
        }
      `}</style>
      {renderChildren(props.law)}
    </div>
  );
}
