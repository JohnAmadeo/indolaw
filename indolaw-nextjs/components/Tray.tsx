import { useState, useEffect } from "react";
import { LawData } from "utils/grammar";
import { colors } from "utils/theme";
import TableOfContentsGroupList from "components/TableOfContentsGroupList";
import { useAppContext } from "utils/context-provider";
import Citation from "./Citation";
import Status from "./Status";
import Divider from "./Divider";
import SettingsSection from "./SettingsSection";
import Tab from "./Tab";
import TrayButton from "./TrayButton";

enum Tabs {
  TABLE_OF_CONTENTS,
  METADATA,
};

export default function Tray(props: {
  law: LawData,
  isExpanded: boolean,
  onExpand: () => void,
  onMinimize: () => void,
  width: number,
}): JSX.Element {
  const { law, isExpanded, onExpand, onMinimize, width } = props;
  const { colorScheme, toggleDarkMode } = useAppContext();
  const [activeTab, setActiveTab] = useState(Tabs.TABLE_OF_CONTENTS);

  useEffect(() => {
    const listener = function (event: KeyboardEvent) {
      if (event.key === 'g') {
        if (isExpanded) {
          onMinimize();
        } else {
          onExpand();
        }
      }
    };

    document.addEventListener('keydown', listener);
    return () => {
      document.removeEventListener("keydown", listener);
    };
  }, [isExpanded]);

  const renderTab = (tab: Tabs): JSX.Element => {
    switch (tab) {
      case Tabs.TABLE_OF_CONTENTS:
        return <TableOfContentsGroupList structures={law.content.children} />;
      case Tabs.METADATA:
        return (
          <>
            <SettingsSection
              title={'Citation'}
              content={(
                <Citation
                  metadata={law.metadata}
                  textColor={colorScheme.tray.textSecondary}
                />
              )}
            />
            <SettingsSection
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

  const contents = (
    <>
      <style jsx>{`
        .tabs {
          display: flex;
          flex-direction: row;
        }

        .pill-container {
          margin: 0 24px 0 0;
          display: flex;
          place-items: center;
        }

        .tray-icon {
          color: ${colorScheme.clickable};
          margin-left: auto;
          cursor: pointer;
          display: flex;
        }

        .material-icons.style {
          vertical-align: bottom;
          font-size: 28px;
          margin: 0 -4px 0 -4px;
        }
      `}</style>
      {isExpanded ? (
        <>
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
                  text={'Settings'}
                />
              </div>
              <div
                className="tray-icon"
                onClick={onMinimize}
              >
                <i className="material-icons style">arrow_back</i>
              </div>
            </div>
            <Divider />
          </div>
          {renderTab(activeTab)}
        </>
      ) : (
        <div
          className="tray-icon"
          onClick={onExpand}
        >
          <i className="material-icons style">arrow_forward</i>
        </div>
      )}
    </>
  );

  return (
    <div className="container">
      <style jsx>{`
        .container {
          width: ${width}px;
          transition: width ease 0.2s;
        }

        .sticky-container {
          padding: ${isExpanded ? '20px' : '20px 12px'};
          position: fixed;
          width: ${width}px;
          background-color: ${colorScheme.tray.background};
          transition: width ease 0.2s;
          height: 100%;
          overflow: auto;
        }
      `}</style>
      <div className="sticky-container">
        {contents}
      </div>
    </div>
  );
}