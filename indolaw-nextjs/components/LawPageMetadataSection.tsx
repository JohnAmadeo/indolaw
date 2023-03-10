import { useAppContext } from "../utils/context-provider";
import { fonts } from "utils/theme";
import Divider from "./Divider";

export default function LawPageMetadataSection(props: {
  title: string,
  list: Array<JSX.Element>,
  isLast: boolean,
}): JSX.Element {
  const { title, list, isLast } = props;
  const { colorScheme } = useAppContext();

  return (
    <div className="container">
      <style jsx>{`
        .container {
          font-family: ${fonts.serif};
          font-size: 18px;
          color: ${colorScheme.text};
          padding: 4px 0;
        }

        .section {
          padding: 8px 0;
        }

        li {
          margin: 16px 0;
          line-height: 1.5;
          list-style-type: ${list.length > 1 ? 'decimal' : 'disc'};
          padding-left: 16px;
        }
      `}</style>
      <div className="section">
        <div><b>{title}</b></div>
        <div>
          <ul>
            {list.map((listItem, idx) => (
              <li key={idx}>{listItem}</li>
            ))}
          </ul>
        </div>
      </div>
      {!isLast && <Divider />}
    </div>
  );
}