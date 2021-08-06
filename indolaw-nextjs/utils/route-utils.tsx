import fs from "fs";
import { Metadata } from "./grammar";

const DIRECTORY_PATH = `../indolaw-parser/metadata/directory.json`;

export function getDirectoryMetadata(
  year: string,
  number: string,
): Metadata {
  // TODO(johnamadeo): This is obviously ugly. Find a better way to combine metadata from law JSON to directory JSON
  const directory = JSON.parse(fs.readFileSync(DIRECTORY_PATH, 'utf8'));
  // @ts-ignore
  const metadata = directory[year].find(entry => entry['number'] === parseInt(number));

  for (let heading of Object.keys(metadata['status'])) {
    for (let entry of metadata['status'][heading]) {
      const { year: lawYear, number: lawNumber } = entry;

      const hukumJelasUrl = `./laws/uu-${lawYear}-${lawNumber}.json`;
      if (fs.existsSync(hukumJelasUrl)) {
        entry['link'] = `/uu/${lawYear}/${lawNumber}`;
      }
    }
  }

  metadata['year'] = year;
  return metadata;
}

export function getLawPaths() {
  // TODO(johnamadeo): This is obviously ugly. Find a better way to combine metadata from law JSON to directory JSON
  const directory = JSON.parse(fs.readFileSync(DIRECTORY_PATH, 'utf8'));

  const paths = [];
  for (let year of Object.keys(directory)) {
    for (let entry of directory[year]) {
      paths.push({
        params: {
          yearOrNickname: year, // year
          number: entry['number'].toString(),
        },
      });
    }
  }

  return paths;
}