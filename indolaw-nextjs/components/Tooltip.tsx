import { Metadata } from "../utils/grammar";
import { fonts } from "../utils/theme";
import _ from "lodash";
import { useAppContext } from "../utils/context-provider";
import { emptyTooltip } from "../utils/tooltip";

export default function Tooltip(props: { metadata: Metadata }): JSX.Element {
  const { metadata } = props;
  const { colorScheme, tooltipData } = useAppContext();

  if (tooltipData === emptyTooltip) {
    return <></>;
  }

  const xPosition: number = tooltipData.xPosition;
  const yPosition: number = tooltipData.yPosition;
  const title = tooltipData.contentKey.split(" ").map(_.capitalize).join(" ");
  const definition = _.capitalize(
    metadata.ketentuan_umum[tooltipData.contentKey.toUpperCase()]
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
