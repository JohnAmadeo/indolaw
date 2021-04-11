import { useState } from "react";
import { LawData } from "utils/grammar";
import { colors } from "utils/theme";
import TableOfContentsGroup from "components/TableOfContentsGroup";
import { useAppContext } from "utils/state-management/context-provider";
import Citation from "./Citation";
import Divider from "./Divider";
import MetadataSection from "./MetadataSection";
import Tab from "./Tab";
import TrayButton from "./TrayButton";
import PutusanMK from "./PutusanMK";

enum Tabs {
  TABLE_OF_CONTENTS,
  METADATA,
};

export default function Tray(props: { law: LawData }): JSX.Element {
  const { law } = props;
  const { colorScheme, toggleDarkMode } = useAppContext();
  const [activeTab, setActiveTab] = useState(Tabs.TABLE_OF_CONTENTS);

  const renderTab = (tab: Tabs): JSX.Element => {
    switch (tab) {
      case Tabs.TABLE_OF_CONTENTS:
        return <>{
          law.content.children.map((child, idx) => (
            <TableOfContentsGroup
              key={idx}
              structure={child}
              depth={0}
              isMobile={false}
            />
          ))}
        </>;
      case Tabs.METADATA:
        return (
          <>
            <MetadataSection
              title={'Citation'}
              content={(
                <Citation
                  metadata={law.metadata}
                  textColor={colorScheme.tray.textSecondary}
                />
              )}
            />
            <MetadataSection
              title={'Putusan MK'}
              content={<PutusanMK law={law} />}
            />
            <MetadataSection
              title={'Theme'}
              content={
                <TrayButton
                  onClick={toggleDarkMode}
                  text={colorScheme == colors ? "Dark" : "Light"}
                />
              }
            />
          </>
        );
    }
  };

  return (
    <>
      <style jsx>{`
        .tabs {
          display: flex;
          flex-direction: row;
        }
        .pill-container {
          margin: 0 24px 0 0;
        }
      }`}</style>
      <div>
        <div className="tabs">
          <div className="pill-container">
            <Tab
              isActive={activeTab === Tabs.TABLE_OF_CONTENTS}
              onClick={() => setActiveTab(Tabs.TABLE_OF_CONTENTS)}
              text={'Daftar Isi'}
            />
          </div>
          <div className="pill-container">
            <Tab
              isActive={activeTab === Tabs.METADATA}
              onClick={() => setActiveTab(Tabs.METADATA)}
              text={'Terkait'}
            />
          </div>
        </div>
        <Divider />
      </div>
      {renderTab(activeTab)}
    </>
  );
}