import Head from "next/head";
import Link from "next/link";
import fs from "fs";
import { useState } from "react";

// TODO willem:
// 1. Search bar (fuzzy search + uu number search)
export default function Home(props) {
  const { laws } = props.data;
  const ALL_YEAR_STRING = "Show All";

  const [selectedYear, setSelectedYear] = useState(ALL_YEAR_STRING);
  const [selectedLaws, setSelectedLaws] = useState(laws);

  const yearList = [ALL_YEAR_STRING, ...Object.keys(laws).sort()];

  const onYearChange = (year) => {
    if (year === selectedYear) {
      return;
    }

    setSelectedYear(year);
    setSelectedLaws(year === ALL_YEAR_STRING ? laws : { [year]: laws[year] });
  };

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
      <p>The search feature is still a work-in-progress. </p>
      <p>For now, below is a list of laws that are available on HukumJelas.</p>
      <p>Alternatively, if you know a law exists in HukumJelas, you can navigate to its URL directly by using either its a) year and number, or b) nickname. For example, Undang-Undang 1 Tahun 1974 Tentang Perkawinan will be at <span className="link"><Link href="/uu/1974/1">hukumjelas.com/uu/1974/1</Link></span> and <span className="link"><Link href="/uu/perkawinan">hukumjelas.com/uu/perkawinan</Link></span></p>
      <p>If you <i>also</i> know the exact Bab or Pasal you want to go to, you can also navigate to it directly! For example, Pasal 4 of UU 13 2003 is at <span className="link"><Link href="/uu/2003/13#pasal-4">hukumjelas.com/uu/2003/13#pasal-4</Link></span> and Bab 10 of UU 13 2003 is at <span className="link"><Link href="/uu/2003/13#bab-10">hukumjelas.com/uu/2003/13#bab-10</Link></span></p>
      <h3>List of Laws</h3>

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

      <ul>
        {Object.keys(selectedLaws)
          .sort()
          .map((year) => (
            <li>
              <p>{year}</p>
              <ul>
                {laws[year]
                  .sort((a, b) => {
                    if (a.number > b.number) {
                      return 1;
                    } else if (a.number === b.number) {
                      return 0;
                    } else {
                      return -1;
                    }
                  })
                  .map((data) => {
                    return (
                      <li>
                        <p>
                          <a href={data.link}>
                            <span className="link">
                              Undang-Undang {data.number} Tahun {data.year} Tentang {data.topic}
                            </span>
                          </a>
                        </p>
                      </li>
                    );
                  })}
              </ul>
            </li>
          ))}
      </ul>
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
