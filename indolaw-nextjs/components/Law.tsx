import { Complex, renderChildren } from "utils/grammar";
import { colors, darkColors, fonts } from "utils/theme";

// TODO(johnamadeo): Fix "Warning: Each child in a list should have a unique "key" prop." problem
export default function Law(props: { law: Complex, isDarkMode: boolean }): JSX.Element {
  return (
    <div>
      <style jsx>{`
        div {
          font-family: ${fonts.serif};
          color: ${(props.isDarkMode ? darkColors : colors).text};
        }
      `}</style>
      <h1>UNDANG UNDANG REPUBLIK INDONESIA TENTANG CIPTA KERJA</h1>
      {renderChildren(props.law)}
    </div>
  );
}
