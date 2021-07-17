import { Complex, Primitive, Structure } from "./grammar";

export const renderCopyHtml = (structure: Complex | Primitive): JSX.Element => {
  switch (structure.type) {
    case Structure.PASAL:
    case Structure.PENJELASAN_PASAL:
    case Structure.PERUBAHAN_SECTION:
    case Structure.PENJELASAN_PERUBAHAN_SECTION:
    case Structure.PERUBAHAN_PASAL:
    case Structure.PENJELASAN_PERUBAHAN_PASAL:
      return renderChildrenHtml(structure as Complex);

    case Structure.PASAL_NUMBER:
    case Structure.PLAINTEXT:
      return <p>{(structure as Primitive).text}</p>;

    case Structure.LIST:
      return renderCopyListHtml(structure as Complex);

    case Structure.UNORDERED_LIST:
      return renderCopyUnorderedListHtml(structure as Complex);

    case Structure.LIST_ITEM:
      return renderCopyListItemHtml(structure as Complex);

    case Structure.PENJELASAN_LIST_ITEM:
      return renderCopyPenjelasanListItemHtml(structure as Complex);

    default:
      console.error(`Couldn't render type ${structure.type}`);
      return <></>;
  }
}

const renderChildrenHtml = (structure: Complex): JSX.Element => {
  const children = structure.children.map(renderCopyHtml);
  return <div>{children}</div>;
};

const renderCopyListHtml = (listStructure: Complex): JSX.Element => {
  if (listStructure.type !== Structure.LIST) {
    throw Error('');
  }

  switch (getListIndexType(listStructure)) {
    case Structure.NUMBER_WITH_DOT:
      return (
        <ol type="1">
          {listStructure.children.map(listItem =>
            renderCopyListItemHtml(listItem as Complex))}
        </ol>
      );
    case Structure.LETTER_WITH_DOT:
    case Structure.LETTER_WITH_RIGHT_BRACKET:
      return (
        <ol type="a">
          {listStructure.children.map(listItem =>
            renderCopyListItemHtml(listItem as Complex))}
        </ol>
      );
    // The 'type' attribute of the ol tag doesn't natively support
    // NUMBER_WITH_BRACKETS, NUMBER_WITH_RIGHT_BRACKET, etc.
    case Structure.NUMBER_WITH_BRACKETS:
    case Structure.NUMBER_WITH_RIGHT_BRACKET:
      return (
        <ol>
          {listStructure.children.map(listItem =>
            renderCopyListItemHtml(listItem as Complex))}
        </ol>
      );
    case Structure.PENJELASAN_HURUF:
    case Structure.PENJELASAN_AYAT:
    case Structure.PENJELASAN_ANGKA:
    case Structure.PENJELASAN_ANGKA_WITH_RIGHT_BRACKET:
      return (
        <ul>
          {listStructure.children.map(listItem =>
            renderCopyPenjelasanListItemHtml(listItem as Complex))}
        </ul>
      );
    default:
      console.log(listStructure.children[0]);
      throw Error('');
  }
};

const renderCopyUnorderedListHtml = (
  structure: Complex
): JSX.Element => {
  if (structure.type !== Structure.UNORDERED_LIST) {
    throw Error('');
  }

  // The 'list-style-type' attribute of the ul tag doesn't natively 
  // support UNORDERED_LIST_INDEX
  return (
    <ul>
      {structure.children.map(listItem => {
        const plaintext = ((listItem as Complex).children[1] as Primitive);
        return (
          <li> {plaintext.text}</li>
        );
      })}
    </ul>
  );
}

const renderCopyListItemHtml = (structure: Complex): JSX.Element => {
  if (structure.type !== Structure.LIST_ITEM) {
    throw Error('');
  }

  const plaintext = structure.children[1] as Primitive;

  let restOfList;
  if (structure.children.length > 2) {
    // 3rd line could be LIST, UNORDERED_LIST, or PLAINTEXT 
    // (see parse_list_item in parser_main.py)
    const thirdChild = structure.children[2];

    if (thirdChild.type === Structure.LIST) {
      restOfList = renderCopyListHtml(thirdChild as Complex);
    } else if (thirdChild.type === Structure.UNORDERED_LIST) {
      restOfList = renderCopyUnorderedListHtml(thirdChild as Complex);
    }
    else if (thirdChild.type === Structure.PLAINTEXT) {
      restOfList = structure.children.slice(2).map(child => (
        <p>{(child as Primitive).text}</p>
      ));
    }
  }

  return (
    <li>
      <p>{plaintext.text}</p>
      {restOfList}
    </li>
  );
};

const renderCopyPenjelasanListItemHtml = (structure: Complex): JSX.Element => {
  if (structure.type !== Structure.PENJELASAN_LIST_ITEM) {
    throw Error('');
  }

  const listIndex = structure.children[0] as Primitive;
  const secondChild = structure.children[1];

  let restOfList;
  // If the second child is a list, it's a nested PENJELASAN LIST
  if (secondChild.type === Structure.LIST) {
    restOfList = renderCopyListHtml(secondChild as Complex);
  } else {
    restOfList = structure.children
      .slice(1)
      .map(child => (
        <li>{renderCopyHtml(child)}</li>
      ));

    restOfList = (
      <ul>
        {structure.children
          .slice(1)
          .map(child => <li>{renderCopyHtml(child)}</li>)
        }
      </ul>
    );
  }

  return (
    <>
      <li>{listIndex.text}</li>
      {restOfList}
    </>
  );
};

const getListIndexType = (listStructure: Complex): Structure => {
  return (listStructure.children[0] as Complex).children[0].type;
}