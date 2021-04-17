import { fonts } from "utils/theme";
import { useAppContext } from "utils/state-management/context-provider";
import Divider from "./Divider";

export default function MetadataSection(props: {
  content: JSX.Element,
  title: string,
}): JSX.Element {
  const { content, title } = props;
  const { colorScheme: { tray } } = useAppContext();

  return (
    <>
      <style jsx>{`
        p {
          color: ${tray.text};
          font-family: ${fonts.sans};
          font-size: 14px;
          margin: 14px 0;
        }
      }`}</style>
      <p>{title}</p>
      {content}
      <Divider />
    </>
  );
}