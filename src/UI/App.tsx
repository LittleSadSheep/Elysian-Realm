import React from 'react';
import { FluentProvider, webLightTheme, Button, TabList, Tab, makeStyles, tokens } from '@fluentui/react-components';
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
    width: '40px',
    height: '40px',
    borderRadius: '8px',
    boxShadow: tokens.shadow4,
  },
  title: {
    fontSize: '24px',
    fontWeight: 700,
    letterSpacing: '1px',
  },
  tabList: {
    margin: '0 32px',
    marginTop: '16px',
  },
  content: {
    flex: 1,
    padding: '32px',
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
        {tab === 'home' && <HomePage />}
        {tab === 'train' && <TrainPage />}
        {tab === 'infer' && <InferPage />}
        {tab === 'tune' && <TunePage />}
        {tab === 'model' && <ModelPage />}
      </main>
    </FluentProvider>
  );
};

export default App;
