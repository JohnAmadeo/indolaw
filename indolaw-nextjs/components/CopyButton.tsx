import { useState } from "react";
import { Complex } from "utils/grammar";
import { useAppContext } from "utils/context-provider";

export default function CopyButton(props: {
  onClick: () => void,
  onMouseEnter?: () => void,
  onMouseLeave?: () => void,
}): JSX.Element {
  const { onClick, onMouseEnter, onMouseLeave } = props;
  const { colorScheme } = useAppContext();
  const [iconName, setIconName] = useState('content_copy');

  return (
    <>
      <style jsx>{`
      div {
        display: flex;
        align-items: center;
        padding: 0 4px;
        margin: 0 4px;
        cursor: pointer;
      }
      
      .material-icons.style {
        vertical-align: bottom;
        font-size: 18px;
        color: ${colorScheme.text};
      }

      .material-icons.style:hover {
        color: ${colorScheme.textHover};
      }
    }`}</style>
      <div
        onClick={async () => {
          setIconName('check');
          onClick();

          setTimeout(() => {
            setIconName('content_copy');
          }, 2000);
        }}
        onMouseEnter={onMouseEnter}
        onMouseLeave={onMouseLeave}
      >
        <i className="material-icons style">{iconName}</i>
      </div>
    </>
  );
}
