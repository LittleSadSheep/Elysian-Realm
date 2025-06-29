import React, { useState } from 'react';
import { FluentProvider, webLightTheme, webDarkTheme } from '@fluentui/react-components';
import { Icon } from '@iconify/react';
import ParallaxButton from './components/ParallaxButton';
import HomePage from './pages/HomePage';
import TrainPage from './pages/TrainPage';
import InferPage from './pages/InferPage';
import TunePage from './pages/TunePage';
import ModelPage from './pages/ModelPage';
import './styles/global.css';
import './components/ParallaxButton.css';

const BUTTONS = [
  { key: 'home', icon: <Icon icon="fluent:home-24-regular" />, label: '首页' },
  { key: 'train', icon: <Icon icon="fluent:play-circle-24-regular" />, label: '训练' },
  { key: 'infer', icon: <Icon icon="fluent:chat-24-regular" />, label: '推理' },
  { key: 'tune', icon: <Icon icon="fluent:wand-24-regular" />, label: '调参' },
  { key: 'model', icon: <Icon icon="fluent:database-24-regular" />, label: '模型管理' },
];

const PROJECT_DESC = '往事乐土 Elysian-Realm';

const App: React.FC = () => {
  const [tab, setTab] = useState('');
  const [dark, setDark] = useState(false);
  const [parallax, setParallax] = useState({ x: 0, y: 0 });

  // 右侧大图视差
  const handleImgMouseMove = (e: React.MouseEvent) => {
    const rect = (e.target as HTMLDivElement).getBoundingClientRect();
    const x = (e.clientX - rect.left - rect.width / 2) / 18;
    const y = (e.clientY - rect.top - rect.height / 2) / 18;
    setParallax({ x, y });
  };
  const handleImgMouseLeave = () => setParallax({ x: 0, y: 0 });

  // 按钮飞入导航栏
  const showNav = !!tab;

  return (
    <FluentProvider theme={dark ? webDarkTheme : webLightTheme} className={`app-root${dark ? ' dark' : ''}`}>  
      <div style={{ display: 'flex', minHeight: '100vh', alignItems: 'stretch' }}>
        {/* 左侧按钮区 */}
        {!showNav && (
          <aside style={{
            width: '100%',
            maxWidth: 520,
            minWidth: 420,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            position: 'relative',
            zIndex: 2,
            paddingLeft: 0,
            margin: '0 auto',
            height: '100vh',
          }}>
            <div className="project-desc">{PROJECT_DESC}</div>
            <div style={{
              marginTop: 12,
              marginBottom: 24,
              width: 420,
              display: 'grid',
              gridTemplateColumns: 'repeat(2, 1fr)',
              gap: 32,
              justifyItems: 'center',
              alignItems: 'center',
              marginLeft: 'auto',
              marginRight: 'auto',
            }}>
              {BUTTONS.map(btn => (
                <ParallaxButton
                  key={btn.key}
                  icon={btn.icon}
                  label={btn.label}
                  selected={tab === btn.key}
                  onClick={() => setTab(btn.key)}
                  flatGlass
                  style={{ width: 200, height: 100, fontSize: 26, margin: 0 }}
                />
              ))}
            </div>
            <button className="fluid-btn" style={{ marginTop: 18, width: 56, height: 56 }} onClick={() => setDark(d => !d)}>
              <Icon icon={dark ? 'fluent:weather-sunny-24-regular' : 'fluent:weather-moon-24-regular'} fontSize={28} />
            </button>
          </aside>
        )}
        {/* 顶部导航栏 */}
        {showNav && (
          <header className="app-header blur-bg" style={{ position: 'fixed', top: 0, left: 0, right: 0, zIndex: 10, display: 'flex', alignItems: 'center', height: 88 }}>
            <img src="/Elysia.png" alt="logo" className="logo" style={{ width: 40, height: 40, borderRadius: 8, boxShadow: '0 2px 8px 0 rgba(0,0,0,0.08)', marginLeft: 32 }} />
            <span className="title" style={{ fontSize: 24, fontWeight: 700, letterSpacing: 1, marginLeft: 16 }}>Elysian-Realm</span>
            <div style={{ flex: 1 }} />
            {BUTTONS.map(btn => (
              <ParallaxButton
                key={btn.key}
                icon={btn.icon}
                label={btn.label}
                selected={tab === btn.key}
                flyToTop
                onClick={() => setTab(btn.key)}
                style={{ margin: '0 8px', width: 64, height: 64, fontSize: 18 }}
              />
            ))}
            <button className="fluid-btn" style={{ marginLeft: 24, width: 56, height: 56 }} onClick={() => setDark(d => !d)}>
              <Icon icon={dark ? 'fluent:weather-sunny-24-regular' : 'fluent:weather-moon-24-regular'} fontSize={28} />
            </button>
          </header>
        )}
        {/* 右侧大图+毛玻璃+视差 */}
        <div style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative', overflow: 'hidden', height: '100vh' }}>
          <div
            style={{
              position: 'absolute',
              right: 0,
              top: 0,
              bottom: 0,
              width: '60%',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              pointerEvents: 'none',
              zIndex: 1,
            }}
            onMouseMove={handleImgMouseMove}
            onMouseLeave={handleImgMouseLeave}
          >
            <div style={{
              position: 'absolute',
              width: 480,
              height: 480,
              right: 80,
              top: '18vh',
              borderRadius: '40px',
              background: dark ? 'rgba(30,30,30,0.32)' : 'rgba(255,255,255,0.32)',
              boxShadow: '0 8px 48px 0 rgba(0,0,0,0.18)',
              backdropFilter: 'blur(32px) saturate(1.2)',
              zIndex: 2,
              transition: 'background 0.4s',
            }} />
            <img
              src="./Elysia.png"
              alt="elysia"
              style={{
                width: 420,
                height: 420,
                objectFit: 'contain',
                borderRadius: '32px',
                boxShadow: '0 8px 48px 0 rgba(0,0,0,0.18)',
                position: 'absolute',
                right: 100,
                top: '22vh',
                zIndex: 3,
                pointerEvents: 'auto',
                transform: `translate3d(${parallax.x * 8}px,${parallax.y * 8}px,0) scale(1.04)`,
                transition: 'transform 0.25s cubic-bezier(.4,0,.2,1)',
              }}
            />
          </div>
          {/* 页面内容区 */}
          {showNav && (
            <main className="app-content fade-in" style={{ zIndex: 5, minHeight: 600, marginTop: 120 }}>
              {tab === 'home' && <HomePage />}
              {tab === 'train' && <TrainPage />}
              {tab === 'infer' && <InferPage />}
              {tab === 'tune' && <TunePage />}
              {tab === 'model' && <ModelPage />}
            </main>
          )}
        </div>
      </div>
    </FluentProvider>
  );
};

export default App;
