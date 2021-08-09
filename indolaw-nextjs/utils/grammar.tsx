import { InlineMath, BlockMath } from 'react-katex';

import PrimitiveStructure from "components/PrimitiveStructure";
import ListItem from "components/ListItem";
import StructureWithHeading from "components/StructureWithHeading";
import CenteredHeading from "components/CenteredHeading";
import { CSSProperties } from "react";
import PenjelasanListItem from "components/PenjelasanListItem";
import PenjelasanPasal from "../components/PenjelasanPasal";
import Pasal from "components/Pasal";
import UUTitle from "components/UUTitle";
import PenjelasanPasalDemiPasal from 'components/PenjelasanPasalDemiPasal';

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
  PENJELASAN_PASAL = "PENJELASAN_PASAL",
  PENJELASAN_TITLE = "PENJELASAN_TITLE",
  PENJELASAN_UMUM = "PENJELASAN_UMUM",
  PENJELASAN_UMUM_TITLE = "PENJELASAN_UMUM_TITLE",
  PENJELASAN_PASAL_DEMI_PASAL = "PENJELASAN_PASAL_DEMI_PASAL",
  PENJELASAN_PASAL_DEMI_PASAL_TITLE = "PENJELASAN_PASAL_DEMI_PASAL_TITLE",
  PENJELASAN_LIST_ITEM = "PENJELASAN_LIST_ITEM",

  PLAINTEXT = "PLAINTEXT",
  MATH = "MATH",

  LIST = "LIST",
  LIST_ITEM = "LIST_ITEM",
  UNORDERED_LIST = "UNORDERED_LIST",
  UNORDERED_LIST_ITEM = "UNORDERED_LIST_ITEM",

  LIST_INDEX = "LIST_INDEX",
  NUMBER_WITH_BRACKETS = "NUMBER_WITH_BRACKETS",
  NUMBER_WITH_RIGHT_BRACKET = "NUMBER_WITH_RIGHT_BRACKET",
  NUMBER_WITH_DOT = "NUMBER_WITH_DOT",
  LETTER_WITH_DOT = "LETTER_WITH_DOT",
  LETTER_WITH_RIGHT_BRACKET = "LETTER_WITH_RIGHT_BRACKET",
  PENJELASAN_HURUF = "PENJELASAN_HURUF",
  PENJELASAN_AYAT = "PENJELASAN_AYAT",
  PENJELASAN_ANGKA = "PENJELASAN_ANGKA",
  PENJELASAN_ANGKA_WITH_RIGHT_BRACKET = "PENJELASAN_ANGKA_WITH_RIGHT_BRACKET",

  PERUBAHAN_SECTION = "PERUBAHAN_SECTION",
  PERUBAHAN_PASAL = "PERUBAHAN_PASAL",
  PERUBAHAN_BAB = "PERUBAHAN_BAB",
  PERUBAHAN_BAGIAN = "PERUBAHAN_BAGIAN",

  PENJELASAN_PERUBAHAN_SECTION = "PENJELASAN_PERUBAHAN_SECTION",
  PENJELASAN_PERUBAHAN_PASAL = "PENJELASAN_PERUBAHAN_PASAL",
  PENJELASAN_PERUBAHAN_BAB = "PENJELASAN_PERUBAHAN_BAB",
  PENJELASAN_PERUBAHAN_BAGIAN = "PENJELASAN_PERUBAHAN_BAGIAN",
}

export const penjelasanStructureMap: Record<string, Structure> = {
  [Structure.PENJELASAN_PASAL]: Structure.PASAL,
  [Structure.PENJELASAN_PERUBAHAN_PASAL]: Structure.PERUBAHAN_PASAL
}

export interface LawData {
  content: Complex | null | undefined;
  metadata: Metadata;
}

export interface Metadata {
  lembaranNegaraNumber: number;
  lembaranNegaraYear: number;
  tambahanLembaranNumber: number;
  number: number;
  topic: string;
  year: number;
  status: { [key: string]: Array<LawStatus> };
  theme: Array<LawTheme>;
  puu: Array<PengujianUndangUndang>;
  bpkPdfLink: string;
  bpkLink: string;
  ketentuan_umum: Record<string, string>;
}

export interface LawStatus {
  year: string;
  number: string;
  law: string;
  link: string;
  context: string;
}

export interface PengujianUndangUndang {
  id: string;
  link: string;
  context: string;
}

export interface LawTheme {
  theme: string;
  link: string;
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

export type NodeMap = { [key: string]: Complex };

export function renderStructure(
  structure: Complex | Primitive,
  key?: string | number,
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
            {renderChildren(structure as Complex, null, isMobile)}
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
    case Structure.MATH:
      return (
        <div style={{ fontSize: '24px' }}>
          <InlineMath math={(structure as Primitive).text} />
        </div>
      );
    case Structure.BAB_NUMBER:
    case Structure.BAB_TITLE:
    case Structure.PASAL_NUMBER:
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
    case Structure.PERUBAHAN_BAB:
    case Structure.PERUBAHAN_BAGIAN:
      return (
        <StructureWithHeading
          key={key}
          structure={structure as Complex}
          numOfHeadingLines={2}
        />
      );
    case Structure.PENJELASAN_PERUBAHAN_BAGIAN:
    case Structure.PENJELASAN_PERUBAHAN_BAB:
      return (
        <StructureWithHeading
          key={key}
          structure={structure as Complex}
          numOfHeadingLines={1}
        />
      );
    case Structure.PASAL:
    case Structure.PERUBAHAN_PASAL:
      return (
        <Pasal
          key={key}
          structure={structure as Complex}
          numOfHeadingLines={1}
        />
      );
    case Structure.PENJELASAN_PERUBAHAN_PASAL:
    case Structure.PENJELASAN_PASAL:
      return (
        <PenjelasanPasal
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
    case Structure.PERUBAHAN_SECTION:
    case Structure.PENJELASAN_PERUBAHAN_SECTION:
      return renderChildren(structure as Complex, key, isMobile);
    case Structure.PENJELASAN_PASAL_DEMI_PASAL:
      return <PenjelasanPasalDemiPasal />
    case Structure.LIST_ITEM:
    case Structure.UNORDERED_LIST_ITEM:
      return <ListItem key={key} structure={structure as Complex} />;
    case Structure.PENJELASAN_LIST_ITEM:
      return <PenjelasanListItem key={key} structure={structure as Complex} />;
    default:
      throw Error(`No rendering function ${structure.type}`);
  }
}

export function renderPenjelasan(
  structure: Complex | Primitive,
  key?: string | number,
  collapseOnDefault?: boolean
) {
  switch (structure.type) {
    case Structure.PENJELASAN_PERUBAHAN_PASAL:
    case Structure.PENJELASAN_PASAL:
      return (
        <>
          <PenjelasanPasal
            key={key}
            structure={structure as Complex}
            numOfHeadingLines={1}
            collapseOnDefault={collapseOnDefault}
          />
        </>
      );
    default:
      return <></>;
  }
}

export function renderChildren(
  structure: Complex,
  key?: string | number | null,
  isMobile?: boolean
): JSX.Element {
  return (
    <div key={key}>
      {structure.children.map((childStructure, idx) =>
        renderStructure(childStructure, idx, isMobile)
      )}
    </div>
  );
}
