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
          background: ${colorScheme.clickableTextBackground};
        }

        a {
          color: ${colorScheme.clickableText};
          border-bottom: 1px solid ${colorScheme.clickableText};
        }
      `}</style>
      <b><a href={props.link} target="_blank">{props.text}</a></b>
    </>
  );
}