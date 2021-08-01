import { useAppContext } from "../utils/context-provider";

export default function StyledLink(props: {
  link: string,
  text: string,
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
      `}</style>
      <a href={props.link} target="_blank">{props.text}</a>
    </>
  );
}