import { Metadata } from "../utils/grammar";
import { useAppContext } from "../utils/state-management/context-provider";
import { fonts } from "../utils/theme";
import _ from "lodash";

export default function Tooltip(props: { metadata: Metadata }): JSX.Element {
  const { metadata } = props;
  const { colorScheme, tooltip } = useAppContext();

  if (!tooltip.content || tooltip.content === "") {
    return <></>;
  }

  const xPosition: number = tooltip.xPosition || 0;
  const yPosition: number = tooltip.yPosition || 0;
  const title = tooltip.content.split(" ").map(_.capitalize).join(" ");
  const definition = _.capitalize(
    metadata.ketentuan_umum[tooltip.content.toUpperCase()]
  );

  return (
    <>
      <style jsx>{`
        div {
          position: absolute;
          top: ${yPosition + "px"};
          left: ${xPosition + "px"};
          height: auto;
          width: auto;
          max-width: 35vw;
          padding: 10px;
          background-color: ${colorScheme.tray.background};
          border-radius: 8px;
          border: 0;
          color: ${colorScheme.tray.text};
          font-family: ${fonts.sans};
          font-size: 14px;
          z-index: 100;
        }
      }`}</style>
      <div>
        <p style={{ fontSize: "18px", fontFamily: fonts.serif }}>{title}</p>
        <hr></hr>
        <p>{definition}</p>
      </div>
    </>
  );
}
