import { fonts } from "utils/theme";
import { useAppContext } from "utils/context-provider";
import Divider from './Divider';

export default function PenjelasanPasalDemiPasal(): JSX.Element {
  const { colorScheme } = useAppContext();

  return (
    <>
      <style jsx>{`
        div {
          margin: 24px 0;
          padding: 40px;
          border: 1px solid ${colorScheme.text};
          border-radius: 8px;
        }
      `}</style>
      <div>
        Untuk kemudahan pemakaian HukumJelas, penjelasan masing-masing pasal
        telah dipindahkan ke bawah pasal terkait
      </div>
    </>
  );
}