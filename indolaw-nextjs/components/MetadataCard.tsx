import { useAppContext } from "../utils/context-provider";
import { fonts } from "utils/theme";

export default function MetadataCard(
  props: {
    title: string,
    body: JSX.Element,
  }
): JSX.Element {
  const { title, body } = props;
  const { colorScheme } = useAppContext();

  return (
    <div className="container">
      <style jsx>{`
        .container {
          font-family: ${fonts.serif};
        }

        .title {
          background-color: ${colorScheme.subcontent.background};
          color: ${colorScheme.text};
          padding: 16px;
          border-radius: 8px 8px 0 0;
          font-weight: 700;
          font-size: 18px;
        }

        .body {
          border: 1px solid ${colorScheme.subcontent.background};
          color: ${colorScheme.text};
          padding: 12px 16px 12px 0;
          border-radius: 0 0 8px 8px;
        }
      `}</style>
      <div className="title">{title}</div>
      <div className="body">{body}</div>
    </div>
  );
}