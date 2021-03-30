import Head from "next/head";
import Link from "next/link";
import styles from "../styles/Home.module.css";

export default function Home() {
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
          color: blue;
        }
      `}</style>
      <Head>
        <title>HukumJelas BETA 🚧</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>
      <h1>HukumJelas BETA 🚧</h1>
      <p>The search feature is still a work-in-progress. </p>
      <p>For now, below is a list of laws that are available on HukumJelas.</p>
      <p>Alternatively, if you know a law exists in HukumJelas, you can navigate to its URL directly by using either its a) year and number, or b) nickname. For example, Undang-Undang 13 Tahun 2003 Tentang Ketenagakerjaan will be at <span className="link"><Link href="/uu/2003/13">hukumjelas.com/uu/2003/13</Link></span> and <span className="link"><Link href="/uu/ketenagakerjaan">hukumjelas.com/uu/ketenagakerjaan</Link></span></p>
      <p>If you <i>also</i> know the exact Bab or Pasal you want to go to, you can also navigate to it directly! For example, Pasal 4 of UU 13 2003 is at <span className="link"><Link href="/uu/2003/13#pasal-4">hukumjelas.com/uu/2003/13#pasal-4</Link></span> and Bab 10 of UU 13 2003 is at <span className="link"><Link href="/uu/2003/13#bab-10">hukumjelas.com/uu/2003/13#bab-10</Link></span></p>
      <h3>List of Laws</h3>
      <ul>
        <li>
          <span className="link"><Link href="/uu/2003/13">Undang-Undang 13 Tahun 2003 Tentang Ketenagakerjaan</Link></span>
        </li>
        <li>
          <span className="link"><Link href="/uu/1999/8">Undang-Undang 8 Tahun 1999 Tentang Perlindungan Konsumen</Link></span>
        </li>
      </ul>
    </div>
  );
}
