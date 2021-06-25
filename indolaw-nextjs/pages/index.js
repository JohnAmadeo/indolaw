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

        .link:hover {
          text-decoration: underline;
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
      <ul>
        <li>1974</li>
        <ul>
          <li>
            <span className="link"><Link href="/uu/1974/1">Undang-Undang 1 Tahun 1974 Tentang Perkawinan</Link></span>
          </li>
        </ul>
        <li>1982</li>
        <ul>
          <li>
            <span className="link"><Link href="/uu/1982/1">Undang-Undang 1 Tahun 1982 Tentang Pengesahan Konvensi Wina Mengenai Hubungan Diplomatik Beserta Protokol Opsionalnya Mengenai Hal Memperoleh Kewarganegaraan (vienna Convention On Diplomatic Relations And Optional Protocol To The Vienna Convertion On Diplomatic Relations Concerning Acquisition Of Nationality, 1961) Dan Pengesahan Konvensi Wina Mengenai Hubungan Konsuler Beserta Protocol Opsionalnya Mengenai Hal Memperoleh Kewarganegaraan (vienna Convention On Consular Relations And Optional Protocol To The Vienna Convention On Consular Relations Concerning Acquisition Of Nationality, 1963)</Link></span>
          </li>
        </ul>
        <li>1986</li>
        <ul>
          <li>
            <span className="link"><Link href="/uu/1986/5">Undang-Undang 5 Tahun 1986 Tentang Peradilan Tata Usaha Negara</Link></span>
          </li>
        </ul>
        <li>1997</li>
        <ul>
          <li>
            <span className="link"><Link href="/uu/1997/8">Undang-Undang 8 Tahun 1997 Tentang Dokumen Perusahaan</Link></span>
          </li>
        </ul>
        <li>1999</li>
        <ul>
          <li>
            <span className="link"><Link href="/uu/1999/8">Undang-Undang 8 Tahun 1999 Tentang Perlindungan Konsumen</Link></span>
          </li>
        </ul>
        <li>2003</li>
        <ul>
          <li>
            <span className="link"><Link href="/uu/2003/13">Undang-Undang 13 Tahun 2003 Tentang Ketenagakerjaan</Link></span>
          </li>
        </ul>
        <li>2007</li>
        <ul>
          <li>
            <span className="link"><Link href="/uu/2007/40">Undang-Undang 40 Tahun 2007 Tentang Perseroan Terbatas</Link></span>
          </li>
        </ul>
        <li>2011</li>
        <ul>
          <li>
            <span className="link"><Link href="/uu/2011/12">Undang-Undang 12 Tahun 2011 Tentang Pembentukan Peraturan Perundang-Undangan</Link></span>
          </li>
        </ul>
        <li>2016</li>
        <ul>
          <li>
            <span className="link"><Link href="/uu/2016/19">Undang-Undang 19 Tahun 2016 Tentang Perubahan Atas Undang-Undang Nomor 11 Tahun 2008 Tentang Informasi dan Transaksi Elektronik</Link></span>
          </li>
        </ul>
        <li>2017</li>
        <ul>
          <li>
            <span className="link"><Link href="/uu/2017/18">Undang-Undang 18 Tahun 2017 Tentang Perlindungan Pekerja Migran Indonesia</Link></span>
          </li>
        </ul>
        <li>2019</li>
        <ul>
          <li>
            <span className="link"><Link href="/uu/2019/19">Undang-Undang 19 Tahun 2019 Tentang Perubahan Kedua atas Undang-Undang Nomor 30 Tahun 2002 Tentang Komisi Pemberantasan Tindak Pidana Korupsi</Link></span>
          </li>
        </ul>
        <li>2020</li>
        <ul>
          <li>
            <span className="link"><Link href="/uu/2020/3">Undang-Undang 3 Tahun 2020 Tentang Perubahan Atas Undang-Undang Nomor 4 Tahun 2009 Tentang Pertambangan Mineral Dan Batubara</Link></span>
          </li>
        </ul>
        <ul>
          <li>
            <span className="link"><Link href="/uu/2020/7">Undang-Undang 7 Tahun 2020 Tentang Perubahan Ketiga Atas Undang-Undang Nomor 24 Tahun 2003 Tentang Mahkamah Konstitusi</Link></span>
          </li>
        </ul>
      </ul>
    </div>
  );
}
