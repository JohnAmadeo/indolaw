import PrimitiveStructure from "components/PrimitiveStructure";
import ListItem from "components/ListItem";
import StructureWithHeading from "components/StructureWithHeading";
import CenteredHeading from "components/CenteredHeading";
import Penjelasan from "components/Penjelasan";
import { CSSProperties } from "react";
import PenjelasanUmum from "components/PenjelasanUmum";

export enum Structure {
  UNDANG_UNDANG = "UNDANG_UNDANG",
  OPENING = "OPENING",
  UU_TITLE = "UU_TITLE",
  PREFACE = "PREFACE",
  AGREEMENT = "AGREEMENT",
  CONSIDERATIONS = "CONSIDERATIONS",
  PRINCIPLES = "PRINCIPLES",
  BAB = "BAB",
  BAB_NUMBER = "BAB_NUMBER",
  BAB_TITLE = "BAB_TITLE",
  PASAL = "PASAL",
  PASAL_NUMBER = "PASAL_NUMBER",
  BAGIAN = "BAGIAN",
  BAGIAN_TITLE = "BAGIAN_TITLE",
  BAGIAN_NUMBER = "BAGIAN_NUMBER",
  PARAGRAF = "PARAGRAF",
  PARAGRAF_TITLE = "PARAGRAF_TITLE",
  PARAGRAF_NUMBER = "PARAGRAF_NUMBER",
  CLOSING = "CLOSING",
  PENJELASAN = "PENJELASAN",
  PENJELASAN_TITLE = "PENJELASAN_TITLE",
  PENJELASAN_UMUM = "PENJELASAN_UMUM",
  PENJELASAN_UMUM_TITLE = "PENJELASAN_UMUM_TITLE",
  PENJELASAN_PASAL_DEMI_PASAL = "PENJELASAN_PASAL_DEMI_PASAL",
  PENJELASAN_PASAL_DEMI_PASAL_TITLE = "PENJELASAN_PASAL_DEMI_PASAL_TITLE",
  PLAINTEXT = "PLAINTEXT",
  LIST = "LIST",
  LIST_ITEM = "LIST_ITEM",
  UNORDERED_LIST = "UNORDERED_LIST",
  UNORDERED_LIST_ITEM = "UNORDERED_LIST_ITEM",
  LIST_INDEX = "LIST_INDEX",
  NUMBER_WITH_BRACKETS = "NUMBER_WITH_BRACKETS",
  NUMBER_WITH_DOT = "NUMBER_WITH_DOT",
  LETTER_WITH_DOT = "LETTER_WITH_DOT",
}

const HEADING_STRUCTURES = new Set([
  Structure.BAB_NUMBER,
  Structure.BAB_TITLE,
  Structure.PASAL_NUMBER,
  Structure.BAGIAN_NUMBER,
  Structure.BAGIAN_TITLE,
  Structure.PARAGRAF_NUMBER,
  Structure.PARAGRAF_TITLE,
]);

const PRIMITIVE_STRUCTURES = new Set([
  Structure.PLAINTEXT,
  Structure.BAB_NUMBER,
  Structure.BAB_TITLE,
  Structure.PASAL_NUMBER,
  Structure.BAGIAN_NUMBER,
  Structure.BAGIAN_TITLE,
  Structure.PARAGRAF_NUMBER,
  Structure.PARAGRAF_TITLE,
]);

export interface Primitive {
  type: Structure;
  text: string;
}

export interface Complex {
  type: Structure;
  children: Array<Primitive | Complex>;
  id: string;
}

export function renderStructure(
  structure: Complex | Primitive,
  key?: string | number,
) {
  // TODO: CenteredHeading, StructureWithHeading, and Pasal need to be combined in a sensible way
  switch (structure.type) {
    case Structure.UU_TITLE:
    case Structure.PREFACE:
    case Structure.AGREEMENT:
    case Structure.CLOSING:
    case Structure.PENJELASAN_TITLE:
      return <CenteredHeading key={key} structure={structure as Complex} />;
    case Structure.PENJELASAN:
      // TODO: Doesn't need to be separate component - can collapse here
      return <Penjelasan key={key} structure={structure as Complex} />;
    case Structure.PLAINTEXT:
    case Structure.BAB_NUMBER:
    case Structure.BAB_TITLE:
    case Structure.PASAL_NUMBER:
    case Structure.BAGIAN_NUMBER:
    case Structure.BAGIAN_TITLE:
    case Structure.PARAGRAF_NUMBER:
    case Structure.PARAGRAF_TITLE:
    case Structure.PENJELASAN_UMUM_TITLE:
    case Structure.PENJELASAN_PASAL_DEMI_PASAL_TITLE:
      return <PrimitiveStructure key={key} structure={structure as Primitive} />;
    case Structure.PENJELASAN_UMUM:
      return <PenjelasanUmum key={key} structure={structure as Complex} />;
    case Structure.BAB:
    case Structure.BAGIAN:
    case Structure.PARAGRAF:
      return (
        <StructureWithHeading
          key={key}
          structure={structure as Complex}
          numOfHeadingLines={2}
        />
      );
    case Structure.PASAL:
      return (
        <StructureWithHeading
          key={key}
          structure={structure as Complex}
          numOfHeadingLines={1}
        />
      );
    case Structure.OPENING:
    case Structure.CONSIDERATIONS:
    case Structure.PRINCIPLES:
    case Structure.PENJELASAN_UMUM:
    case Structure.PENJELASAN_PASAL_DEMI_PASAL:
    case Structure.LIST:
    case Structure.UNORDERED_LIST:
      return renderChildren(structure as Complex, key);
    case Structure.LIST_ITEM:
    case Structure.UNORDERED_LIST_ITEM:
      return <ListItem key={key} structure={structure as Complex} />;
    default:
      return <></>;
  }
}

export function renderChildren(
  structure: Complex,
  key?: string | number,
): JSX.Element {
  return (
    <div key={key}>
      {structure.children.map((childStructure, idx) =>
        renderStructure(childStructure, idx)
      )}
    </div>
  );
}
