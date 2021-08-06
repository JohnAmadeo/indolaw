import { useAppContext } from "../utils/context-provider";

export default function StyledLink(props: {
  link: string,
  text: string,
  iconName?: string,
}): JSX.Element {
  const { colorScheme } = useAppContext();

  return (
    <>
      <style jsx >{`
        a:hover {
          background: ${colorScheme.clickableBackground};
        }

        a {
          color: ${colorScheme.clickable};
          border-bottom: 1px solid ${colorScheme.clickable};
        }

        .material-icons.style {
          color: ${colorScheme.clickable};
          vertical-align: bottom;
          font-size: 24px;
        }
      `}</style>
      <i className="material-icons style">{props.iconName}</i>
      <a href={props.link} target="_blank">
        {props.text}
      </a>
    </>
  );
}