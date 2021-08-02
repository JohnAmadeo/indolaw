import Head from "next/head";
import Link from "next/link";
import fs from "fs";
import { useState } from "react";
import _ from 'lodash';
import Fuse from 'fuse.js';

export default function Home(props) {
  const { laws } = props.data;
  const ALL_YEAR_STRING = "Show All";

  const [selectedYear, setSelectedYear] = useState(ALL_YEAR_STRING);
  const [isSearching, setIsSearching] = useState(false);
  const [selectedLaws, setSelectedLaws] = useState([]);

  const yearList = [ALL_YEAR_STRING, ...Object.keys(laws).sort()];

  const fuse = new Fuse(_.flatMap(_.values(laws)), {
    keys: ['link', 'topic', 'number', 'year'],
    shouldSort: true
  });

  const onYearChange = (year) => {
    if (year === selectedYear) {
      return;
    }

    setSelectedYear(year);
  };

  const onSearch = (e) => {
    if (_.isEmpty(e)) {
      resetSearch();
      return;
    }

    setIsSearching(true);

    const searchResult = fuse.search(e, {
      limit: 20
    });

    setSelectedLaws(searchResult.map(res => res.item));
  }

  const resetSearch = () => {
    setIsSearching(false);
    setSelectedLaws([]);
  }

  const styles = (
    <style jsx>{`
    p {
      margin: 12px 0;
    }

    .link {
      cursor: pointer;
      color: blue;
    }

    .link:hover {
      text-decoration: underline;
    }
  `}</style>
  );

  const renderLawListItem = (item) => {
    return (<>
    {styles}
      <li>
        <p>
          <a href={item.link}>
            <span className="link">
              Undang-Undang {item.number} Tahun {item.year} Tentang {item.topic}
            </span>
          </a>
        </p>
      </li>
      </>
    );
  }

  const allLawsDisplay = (
    <>
      {styles}
      <ul>
        {Object.keys(
          selectedYear === ALL_YEAR_STRING
            ? laws
            : { [selectedYear]: laws[selectedYear] }
        )
          .sort()
          .map((year) => (
            <li>
              <p>{year}</p>
              <ul>
                {laws[year]
                  .sort((a, b) => parseInt(a.number) - parseInt(b.number))
                  .map(renderLawListItem)}
              </ul>
            </li>
          ))}
      </ul>
    </>
  );

  const searchResult = (
    <>
      {styles}
      <ul>{selectedLaws.map(renderLawListItem)}</ul>
    </>
  );

  return (
    <div className="container">
      <style jsx>{`
        .container {
          margin: 48px;
          max-width: 768px;
        }

        p {
          margin: 12px 0;
        }

        .link {
          cursor: pointer;
          color: blue;
        }

        .link:hover {
          text-decoration: underline;
        }

        #selected {
          text-decoration: none;
          cursor: default;
          color: black;
        }

        ul#year-list {
          list-style-type: none;
        }

        ul#year-list li {
          display: inline-block;
          margin: 10px;
        }
      `}</style>
      <Head>
        <title>HukumJelas BETA 🚧</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <h1>HukumJelas BETA 🚧</h1>
      <p>This page displays a list of laws that are available on HukumJelas.</p>
      <p>
        Alternatively, if you know a law exists in HukumJelas, you can navigate
        to its URL directly by using either its a) year and number, or b)
        nickname. For example, Undang-Undang 1 Tahun 1974 Tentang Perkawinan
        will be at <span className="link"><Link href="/uu/1974/1">hukumjelas.com/uu/1974/1</Link></span>
        and <span className="link"><Link href="/uu/perkawinan">hukumjelas.com/uu/perkawinan</Link></span>
      </p>
      <p>
        If you <i>also</i> know the exact Bab or Pasal you want to go to, you
        can also navigate to it directly! For example, Pasal 4 of UU 13 2003 is
        at<span className="link"><Link href="/uu/2003/13#pasal-4">hukumjelas.com/uu/2003/13#pasal-4</Link></span>
        and Bab 10 of UU 13 2003 is at <span className="link"><Link href="/uu/2003/13#bab-10">hukumjelas.com/uu/2003/13#bab-10</Link></span>
      </p>
      <p>
        The search feature is still a work-in-progress. For now, if you want to
        get the best approximation for the search result, you can try to search
        the topics of the UU (ex: "Perkawinan", "Kawin", etc) or search the year
        and number of UU with the format "year/number" (ex: "1997/8", "2002/2",
        etc)
      </p>

      <input
        className="search-box"
        onKeyDown={_.debounce((e) => onSearch(e.target.value), 150)}
        placeholder="Search..."
      ></input>

      <h3>List of Laws</h3>

      {!isSearching && (
        <ul id="year-list">
          {yearList.map((year) => (
            <li>
              <span
                className="link"
                id={year === selectedYear ? "selected" : ""}
                onClick={() => onYearChange(year)}
              >
                {year}
              </span>
            </li>
          ))}
        </ul>
      )}

      {isSearching ? searchResult : allLawsDisplay}

      {isSearching && selectedLaws.length == 0 && <p>Sorry, but it looks like nothing comes up with that search query</p>}
    </div>
  );
}

export const getStaticProps = async ({ params }) => {
  const lawsList = fs.readdirSync("./laws").map((filename) => {
    const parts = filename.replace(/\.json$/, "").split("-");
    return {
      year: parts[1],
      number: parts[2],
    };
  });

  const laws = {};
  for (let law of lawsList) {
    const year = parseInt(law.year);

    const file = JSON.parse(
      fs.readFileSync(`./laws/uu-${law.year}-${law.number}.json`, "utf8")
    );

    if (!(year in laws)) {
      laws[year] = [];
    }

    laws[year].push({
      number: parseInt(law.number),
      topic: file.metadata.topic,
      year: year,
      link: `/uu/${year}/${law.number}`,
    });
  }

  return {
    props: {
      data: {
        laws,
      },
    },
  };
};
