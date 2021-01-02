import Head from "next/head";
import Link from "next/link";
import styles from "../styles/Home.module.css";

export default function WorkInProgress() {
  return (
    <div className={styles.container}>
      <Head>
        <title>HukumJelas BETA</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Work in progress. Go back to <Link href="/uu/ciptakerja">demo</Link>
        </h1>
      </main>
    </div>
  );
}