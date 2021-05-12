import { useAppContext } from "utils/context-provider";

export default function Divider(): JSX.Element {
  const { colorScheme } = useAppContext();
  return (
    <>
      <style jsx>{`
        .solid {          
          border: 0px;
          border-top: 1px solid ${colorScheme.tray.textSecondary};
          margin: 14px 0;
        }
      `}</style>
      <hr className="solid" />
    </>
  );
}
