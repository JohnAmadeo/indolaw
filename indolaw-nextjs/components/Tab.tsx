import { fonts } from "utils/theme";
import { useAppContext } from "utils/context-provider";

export default function Tab(props: {
  isActive: boolean,
  onClick?: () => void,
  text: string
}): JSX.Element {
  const { isActive, onClick, text } = props;
  const { invertedColorScheme: { tray } } = useAppContext();

  // TODO(johnamadeo)
  // Setting outline CSS property to none is bad for accessibility; figure out something else
  return (
    <>
      <style jsx>{`
        .pill {
          cursor: pointer;
          color: ${isActive ? tray.text : tray.textSecondary};
          font-family: ${fonts.sans};
          font-size: 14px;
        }

        .pill:hover {
          color: ${isActive ? tray.textSecondary : tray.text};
        }

        .pill:focus {
          outline: none;
        }
      }`}</style>
      <div
        className="pill"
        onClick={onClick}
      >
        {text}
      </div>
    </>
  );
}
