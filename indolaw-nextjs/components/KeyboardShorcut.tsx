import { useAppContext } from "utils/context-provider";

export default function KeyboardShortcut(props: {
  text: string,
}): JSX.Element {
  const { colorScheme } = useAppContext();

  return (
    <div className="keyboard-shortcut">
      <style jsx>{`
        .keyboard-shortcut {
          display: block;
          color: ${colorScheme.tray.buttonText};
          background-color: ${colorScheme.tray.button};
          border-radius: 4px;
          width: 24px;
          height: 28px;
          display: flex;
          place-items: center center;
        }

        .keyboard-shortcut-inner {
          margin: 0 auto;
        }
      `}</style>
      <div className="keyboard-shortcut-inner">{props.text}</div>
    </div>
  );
}