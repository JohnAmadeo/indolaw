import { useState } from "react";
import { Structure, Complex, Primitive } from "utils/grammar";
import { colors, fonts } from "utils/theme";
import { NextRouter, useRouter } from "next/router";
import { useAppContext } from "../utils/context-provider";
import TableOfContentsGroup from './TableOfContentsGroup';

export default function TableOfContentsGroupList(props: {
  structures: (Complex | Primitive)[],
}): JSX.Element {
  const { structures } = props;
  const { colorScheme } = useAppContext();

  const structuresWithChildren = new Set([
    Structure.BAB,
    Structure.BAGIAN,
    Structure.PARAGRAF,
  ]);
  const hasChildren = structures.some(child => structuresWithChildren.has(child.type));
  console.log(hasChildren);

  return (
    <div>
      <style jsx>{`
        div {
          border-left: ${hasChildren ? 'none' : `2px solid ${colorScheme.clickable}`};
          padding-left: ${hasChildren ? '0' : '8px'};
        }
      `}</style>
      {structures.map((child, idx) => (
        <TableOfContentsGroup
          key={idx}
          structure={child}
          depth={0}
          isMobile={false}
          shouldShowExpanderWidth={hasChildren}
        />
      ))}
    </div>
  );
}