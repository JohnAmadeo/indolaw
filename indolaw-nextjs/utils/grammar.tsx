import PrimitiveStructure from "components/PrimitiveStructure";
import ListItem from "components/ListItem";
import StructureWithHeading from "components/StructureWithHeading";
import CenteredHeading from "components/CenteredHeading";
import { CSSProperties } from "react";
import PenjelasanListItem from "components/PenjelasanListItem";
import PenjelasanPasalItem from "../components/PenjelasanPasalItem";
import Pasal from "components/Pasal";
import UUTitle from "components/UUTitle";

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
  MODIFIED_PASAL = "MODIFIED_PASAL",
  MODIFIED_PASAL_NUMBER = "MODIFIED_PASAL_NUMBER",
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
  PENJELASAN_LIST_ITEM = "PENJELASAN_LIST_ITEM",
  PLAINTEXT = "PLAINTEXT",
  LIST = "LIST",
  LIST_ITEM = "LIST_ITEM",
  UNORDERED_LIST = "UNORDERED_LIST",
  UNORDERED_LIST_ITEM = "UNORDERED_LIST_ITEM",
  LIST_INDEX = "LIST_INDEX",
  NUMBER_WITH_BRACKETS = "NUMBER_WITH_BRACKETS",
  NUMBER_WITH_RIGHT_BRACKET = "NUMBER_WITH_RIGHT_BRACKET",
  NUMBER_WITH_DOT = "NUMBER_WITH_DOT",
  LETTER_WITH_DOT = "LETTER_WITH_DOT",
  PENJELASAN_HURUF = "PENJELASAN_HURUF",
  PENJELASAN_AYAT = "PENJELASAN_AYAT",
  PENJELASAN_ANGKA = "PENJELASAN_ANGKA",
}

const HEADING_STRUCTURES = new Set([
  Structure.BAB_NUMBER,
  Structure.BAB_TITLE,
  Structure.PASAL_NUMBER,
  Structure.MODIFIED_PASAL_NUMBER,
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
  Structure.MODIFIED_PASAL_NUMBER,
  Structure.BAGIAN_NUMBER,
  Structure.BAGIAN_TITLE,
  Structure.PARAGRAF_NUMBER,
  Structure.PARAGRAF_TITLE,
]);

export interface LawData {
  content: Complex;
  metadata: Metadata;
}

export interface Metadata {
  lembaranNegaraNumber: number;
  lembaranNegaraYear: number;
  tambahanLembaranNumber: number;
  number: number;
  topic: string;
  year: number;
  status: Array<string>;
}

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
  penjelasanUmum?: Array<Complex | Primitive>,
  isMobile?: boolean
) {
  switch (structure.type) {
    case Structure.UU_TITLE:
      return <UUTitle key={key} structure={structure as Complex} />;
    case Structure.PREFACE:
    case Structure.AGREEMENT:
    case Structure.CLOSING:
    case Structure.PENJELASAN_TITLE:
      return <CenteredHeading key={key} structure={structure as Complex} />;
    case Structure.PENJELASAN:
      return (
        <>
          <style jsx>{`
            div {
              margin: 144px 0 0 0;
            }
          `}</style>
          <div id={(structure as Complex).id}>
            {renderChildren(structure as Complex)}
          </div>
        </>
      );
    case Structure.PLAINTEXT:
      const customStyle: CSSProperties = {
        textAlign: isMobile ? "start" : "justify",
      };
      return (
        <PrimitiveStructure
          key={key}
          structure={structure as Primitive}
          customStyle={customStyle}
        />
      );
    case Structure.BAB_NUMBER:
    case Structure.BAB_TITLE:
    case Structure.PASAL_NUMBER:
    case Structure.MODIFIED_PASAL_NUMBER:
    case Structure.BAGIAN_NUMBER:
    case Structure.BAGIAN_TITLE:
    case Structure.PARAGRAF_NUMBER:
    case Structure.PARAGRAF_TITLE:
      return (
        <PrimitiveStructure key={key} structure={structure as Primitive} />
      );
    case Structure.PENJELASAN_UMUM_TITLE:
    case Structure.PENJELASAN_PASAL_DEMI_PASAL_TITLE:
      const headingStyle: CSSProperties = {
        fontWeight: 700,
      };
      return (
        <PrimitiveStructure
          key={key}
          structure={structure as Primitive}
          customStyle={headingStyle}
        />
      );
    case Structure.BAB:
    case Structure.BAGIAN:
    case Structure.PARAGRAF:
      return (
        <StructureWithHeading
          key={key}
          penjelasanUmum={penjelasanUmum}
          structure={structure as Complex}
          numOfHeadingLines={2}
        />
      );
    case Structure.PASAL:
    case Structure.MODIFIED_PASAL:
      return (
        <Pasal
          key={key}
          structure={structure as Complex}
          numOfHeadingLines={1}
        />
      );
    case Structure.OPENING:
    case Structure.CONSIDERATIONS:
    case Structure.PRINCIPLES:
    case Structure.PENJELASAN_UMUM:
    case Structure.PENJELASAN_UMUM:
    case Structure.LIST:
    case Structure.UNORDERED_LIST:
      return renderChildren(structure as Complex, key, penjelasanUmum);
    case Structure.PENJELASAN_PASAL_DEMI_PASAL:
      return (
        <>
          <style jsx>{`
            div {
              margin: 48px;
              padding: 40px;
              border: 5px solid black;
            }
          `}</style>
          <div>
            Untuk kemudahan pemakaian HukumJelas, penjelasan masing-masing pasal
            telah dipindahkan ke bawah pasal terkait
          </div>
        </>
      );
    case Structure.LIST_ITEM:
    case Structure.UNORDERED_LIST_ITEM:
      return <ListItem key={key} structure={structure as Complex} />;
    case Structure.PENJELASAN_LIST_ITEM:
      return <PenjelasanListItem key={key} structure={structure as Complex} />;
    default:
      throw Error(`No rendering function ${structure.type}`);
  }
}

export function renderPenjelasanUmum(
  structure: Complex | Primitive,
  key?: string | number
) {
  switch (structure.type) {
    case Structure.PASAL:
      return (
        <>
          <PenjelasanPasalItem
            key={key}
            structure={structure as Complex}
            numOfHeadingLines={1}
          />
        </>
      );
    default:
      return <></>;
  }
}

export function renderChildren(
  structure: Complex,
  key?: string | number,
  penjelasanUmum?: Array<Complex | Primitive>
): JSX.Element {
  return (
    <div key={key}>
      {structure.children.map((childStructure, idx) =>
        renderStructure(childStructure, idx, penjelasanUmum)
      )}
    </div>
  );
}
