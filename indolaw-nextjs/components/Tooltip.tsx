import { Metadata } from "../utils/grammar";
import { fonts } from "../utils/theme";
import _ from "lodash";
import { LawContext, useAppContext } from "../utils/context-provider";
import { useContext } from "react";
import Divider from "./Divider";

export interface TooltipData {
  contentKey: string;
  xPosition: number;
  yPosition: number;
}

export const emptyTooltipData: TooltipData = {
  contentKey: '',
  xPosition: 0,
  yPosition: 0,
};

export default function Tooltip(props: {
  tooltipData: TooltipData
}): JSX.Element {
  const { /*metadata*/ tooltipData } = props;
  const { colorScheme } = useAppContext();
  const { metadata } = useContext(LawContext);

  if (tooltipData === emptyTooltipData || metadata == null) {
    return <></>;
  }

  const xPosition: number = tooltipData.xPosition;
  const yPosition: number = tooltipData.yPosition;
  const title = tooltipData.contentKey.split(" ").join(" ");
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
          line-height: 1.5;
          height: auto;
          width: auto;
          max-width: 35vw;
          padding: 20px;
          background-color: ${colorScheme.subcontent.background};
          border-radius: 8px;
          border: 1px solid ${colorScheme.clickable};
          color: ${colorScheme.text};
          font-family: ${fonts.serif};
          font-size: 18px;
          z-index: 100;
        }

        .definition {
          color: ${colorScheme.text};
        }
      }`}</style>
      <div>
        <p><i>{title}</i></p>
        <Divider />
        <p className="definition">{definition}</p>
      </div>
    </>
  );
}
