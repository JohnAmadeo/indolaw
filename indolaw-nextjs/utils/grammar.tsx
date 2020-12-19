import Pasal from "components/Pasal";
import PrimitiveStructure from "components/PrimitiveStructure";
import ListItem from "components/ListItem";
import StructureWithTitleAndNumber from "components/StructureWithTitleAndNumber";

export enum Structure {
  UNDANG_UNDANG = "UNDANG_UNDANG",
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
  PLAINTEXT = "PLAINTEXT",
  LIST = "LIST",
  LIST_ITEM = "LIST_ITEM",
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

export function renderStructure(structure: Complex | Primitive) {
  switch (structure.type) {
    case Structure.PLAINTEXT:
    case Structure.BAB_NUMBER:
    case Structure.BAB_TITLE:
    case Structure.PASAL_NUMBER:
    case Structure.BAGIAN_NUMBER:
    case Structure.BAGIAN_TITLE:
    case Structure.PARAGRAF_NUMBER:
    case Structure.PARAGRAF_TITLE:
      return <PrimitiveStructure structure={structure as Primitive} />;
    case Structure.BAB:
    case Structure.BAGIAN:
    case Structure.PARAGRAF:
      return <StructureWithTitleAndNumber structure={structure as Complex} />;
    case Structure.LIST:
      return renderChildren(structure as Complex);
    case Structure.LIST_ITEM:
      return <ListItem structure={structure as Complex} />;
    case Structure.PASAL:
      return <Pasal structure={structure as Complex} />;
    default:
      return <></>;
  }
}

export function renderChildren(structure: Complex): JSX.Element {
  return (
    <div>
      {structure.children.map((childStructure) =>
        renderStructure(childStructure)
      )}
    </div>
  );
}
