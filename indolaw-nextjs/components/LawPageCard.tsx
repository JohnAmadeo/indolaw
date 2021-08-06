import { useAppContext } from "../utils/context-provider";
import _ from "lodash";

export default function LawPageCard(props: {
  children: JSX.Element,
}): JSX.Element {
  const { colorScheme } = useAppContext();

  return (
    <div className="container">
      <style jsx >{`
        .container {
          border: 1px solid ${colorScheme.clickable};
          padding: 36px;
          border-radius: 8px;
        }

        li {
          margin: 8px 0;
        }

        .none {
          margin: 16px;
        }

        span {
          color: ${colorScheme.textHover};
        }
      `}</style>
      {props.children}
    </div>
  );
}