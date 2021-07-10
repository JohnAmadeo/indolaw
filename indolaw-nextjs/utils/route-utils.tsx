import fs from "fs";

export function getDirectoryMetadata(
  year: string,
  number: string,
) {
  // TODO(johnamadeo): This is obviously ugly. Find a better way to combine metadata from law JSON to directory JSON
  const directory = JSON.parse(fs.readFileSync(`../indolaw-parser/metadata/directory.json`, 'utf8'));
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

  return metadata;
}