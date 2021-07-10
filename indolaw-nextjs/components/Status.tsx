import { Metadata } from "utils/grammar";
import { fonts } from "utils/theme";

export default function Status(props: {
  metadata: Metadata,
  textColor: string,
}): JSX.Element {
  const {
    status
  } = props.metadata;

  return <></>;

  // return (
  //   <div>
  //     <style jsx>{`
  //       div {
  //         color: ${props.textColor};
  //         font-family: ${fonts.sans};
  //         font-size: 14px;
  //       }

  //       ul {
  //         padding-left: 20px;
  //       }

  //       li {
  //         margin: 8px 0;
  //       }
  //     `}</style>
  //     {status && status.length > 0 ?
  //       <ul>
  //         {status.map(line => <li key={line}>{line}</li>)}
  //       </ul> :
  //       <span>N/A</span>
  //     }
  //   </div>
  // );
}
