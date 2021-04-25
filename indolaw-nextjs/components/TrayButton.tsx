import { fonts } from "utils/theme";
import { useAppContext } from "utils/context-provider";

export default function TrayButton(props: {
  iconName?: string,
  onClick: () => void,
  text: string,
}): JSX.Element {
  const { colorScheme } = useAppContext();
  const { iconName, onClick, text } = props;

  const icon = iconName != null ? (
    <>
      <style jsx>{`
        .material-icons.style {
          vertical-align: bottom;
          font-size: 18px;
        }
      }`}</style>
      <i className="material-icons style">{iconName}</i>
    </>
  ) : null;

  return <>
    <style jsx>{`
      button {
        cursor: pointer;
        height: 36px;
        padding: 4px 20px;
        background-color: ${colorScheme.tray.button};
        border-radius: 8px;
        border: 0;
        color: ${colorScheme.tray.buttonText};
        font-family: ${fonts.sans};
        font-size: 14px;
      }

      button:focus {
        outline: none;
      }

      button:hover {
        background-color: ${colorScheme.tray.buttonHover};
      }

      .material-icons.style {
        vertical-align: bottom;
        font-size: 18px;
      }
    }`}</style>
    <button onClick={onClick}>
      {icon} {text}
    </button>
  </>;
}