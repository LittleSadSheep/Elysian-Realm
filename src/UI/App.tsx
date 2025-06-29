import React from 'react';
import { FluentProvider, webLightTheme, Button, TabList, Tab, TabPanel, makeStyles, tokens } from '@fluentui/react-components';
import { Icon } from '@iconify/react';
import HomePage from './pages/HomePage';
import TrainPage from './pages/TrainPage';
import InferPage from './pages/InferPage';
import TunePage from './pages/TunePage';
import ModelPage from './pages/ModelPage';

const useStyles = makeStyles({
  root: {
    minHeight: '100vh',
    background: tokens.colorNeutralBackground1,
    color: tokens.colorNeutralForeground1,
    display: 'flex',
    flexDirection: 'column',
  },
  header: {
    display: 'flex',
    alignItems: 'center',
    padding: '16px 32px',
    borderBottom: `1px solid ${tokens.colorNeutralStroke2}`,
    gap: '16px',
    background: tokens.colorNeutralBackground2,
  },
  logo: {
    width: 40,
    height: 40,
    borderRadius: 8,
    boxShadow: tokens.shadow4,
  },
  title: {
    fontSize: 24,
    fontWeight: 700,
    letterSpacing: 1,
  },
  tabList: {
    margin: '0 32px',
    marginTop: 16,
  },
  content: {
    flex: 1,
    padding: 32,
    background: tokens.colorNeutralBackground1,
    overflow: 'auto',
  },
});

const App: React.FC = () => {
  const styles = useStyles();
  const [tab, setTab] = React.useState('home');

  return (
    <FluentProvider theme={webLightTheme} className={styles.root}>
      <header className={styles.header}>
        <img src="/Elysia.png" alt="logo" className={styles.logo} />
        <span className={styles.title}>Elysian-Realm</span>
        <span style={{ flex: 1 }} />
        <Button appearance="subtle" icon={<Icon icon="fluent:settings-24-regular" width={24} />} />
        <Button appearance="subtle" icon={<Icon icon="fluent:info-24-regular" width={24} />} />
        <Button appearance="subtle" icon={<Icon icon="fluent:github-24-regular" width={24} />} as="a" href="https://github.com/LittleSadSheep/Elysian-Realm" target="_blank" />
      </header>
      <TabList selectedValue={tab} onTabSelect={(_, d) => setTab(d.value as string)} className={styles.tabList}>
        <Tab value="home" icon={<Icon icon="fluent:home-24-regular" />}>首页</Tab>
        <Tab value="train" icon={<Icon icon="fluent:play-circle-24-regular" />}>训练</Tab>
        <Tab value="infer" icon={<Icon icon="fluent:chat-24-regular" />}>推理</Tab>
        <Tab value="tune" icon={<Icon icon="fluent:wand-24-regular" />}>调参</Tab>
        <Tab value="model" icon={<Icon icon="fluent:database-24-regular" />}>模型管理</Tab>
      </TabList>
      <main className={styles.content}>
        <TabPanel value="home" hidden={tab !== 'home'}><HomePage /></TabPanel>
        <TabPanel value="train" hidden={tab !== 'train'}><TrainPage /></TabPanel>
        <TabPanel value="infer" hidden={tab !== 'infer'}><InferPage /></TabPanel>
        <TabPanel value="tune" hidden={tab !== 'tune'}><TunePage /></TabPanel>
        <TabPanel value="model" hidden={tab !== 'model'}><ModelPage /></TabPanel>
      </main>
    </FluentProvider>
  );
};

export default App;
