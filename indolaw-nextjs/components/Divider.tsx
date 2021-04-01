import { colors } from "utils/theme";

export default function Divider(): JSX.Element {
  return (
    <>
      <style jsx>{`
        .solid {          
          border: 0px;
          border-top: 1px solid ${colors.tray.textSecondary};
          margin: 24px 0;
        }
      `}</style>
      <hr className="solid" />
    </>
  );
}
