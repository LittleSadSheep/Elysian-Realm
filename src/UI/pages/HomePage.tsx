import * as React from 'react';
import { makeStyles, tokens, Text } from '@fluentui/react-components';
import { Icon } from '@iconify/react';

const useStyles = makeStyles({
  title: {
    fontWeight: 700,
    fontSize: '2rem',
    marginBottom: '12px',
    color: tokens.colorBrandForeground1,
    letterSpacing: '0.02em',
    '@media (prefers-color-scheme: dark)': {
      color: tokens.colorBrandForeground2,
    },
  },
  desc: {
    fontSize: '1.1rem',
    color: tokens.colorNeutralForeground2,
    marginBottom: '18px',
    '@media (prefers-color-scheme: dark)': {
      color: tokens.colorNeutralForeground3,
    },
  },
  tip: {
    marginTop: '28px',
    color: tokens.colorNeutralForeground3,
    fontSize: '0.98rem',
    '@media (prefers-color-scheme: dark)': {
      color: tokens.colorNeutralForeground4,
    },
  },
  '@keyframes fadeIn': {
    from: { opacity: 0, transform: 'translateY(40px)' },
    to: { opacity: 1, transform: 'none' },
  },
  '@keyframes bounceIn': {
    '0%': { transform: 'scale(0.7)' },
    '60%': { transform: 'scale(1.1)' },
    '100%': { transform: 'scale(1)' },
  },
});

const getGlassStyle = () => {
  const isDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  return {
    maxWidth: '640px',
    width: '90vw',
    margin: '0 auto',
    padding: '40px 32px',
    borderRadius: '28px',
    boxShadow: '0 8px 32px 0 rgba(31, 38, 135, 0.18)',
    backdropFilter: 'blur(18px) saturate(160%)',
    WebkitBackdropFilter: 'blur(18px) saturate(160%)',
    border: isDark ? '1.5px solid rgba(80,80,120,0.24)' : '1.5px solid rgba(255,255,255,0.24)',
    background: isDark ? 'rgba(32,32,40,0.38)' : 'rgba(255,255,255,0.18)',
    textAlign: "center" as "center",
    transition: 'background 0.3s',
    animation: 'fadeIn 0.8s cubic-bezier(.4,0,.2,1)',
  };
};

const getRootStyle = () => {
  const isDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  return {
    minHeight: '100vh',
    width: '100vw',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    position: "fixed" as "fixed",
    top: 0,
    left: 0,
    zIndex: 0,
    background: isDark
      ? `linear-gradient(135deg, ${tokens.colorNeutralBackground4} 0%, ${tokens.colorBrandBackground2} 100%)`
      : `linear-gradient(135deg, ${tokens.colorBrandBackground2} 0%, ${tokens.colorNeutralBackground3} 100%)`,
  };
};

const HomePage: React.FC = () => {
  const styles = useStyles();
  const [glassStyle, setGlassStyle] = React.useState(getGlassStyle());
  const [rootStyle, setRootStyle] = React.useState(getRootStyle());

  React.useEffect(() => {
    const update = () => {
      setGlassStyle(getGlassStyle());
      setRootStyle(getRootStyle());
    };
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', update);
    // 调试输出 tokens 和 style
    // eslint-disable-next-line no-console
    console.log('tokens:', tokens);
    // eslint-disable-next-line no-console
    console.log('rootStyle:', getRootStyle());
    // eslint-disable-next-line no-console
    console.log('glassStyle:', getGlassStyle());
    return () => {
      window.matchMedia('(prefers-color-scheme: dark)').removeEventListener('change', update);
    };
  }, []);

  // 临时硬编码背景色测试
  const debugRootStyle = {
    ...rootStyle,
    background: 'linear-gradient(135deg, #e0e7ef 0%, #b6c6e3 100%)',
  };
  const debugGlassStyle = {
    ...glassStyle,
    background: 'rgba(255,255,255,0.7)',
  };

  return (
    <div style={debugRootStyle}>
      <div style={debugGlassStyle}>
        <Icon icon="fluent:rocket-24-filled" style={{ fontSize: 56, color: tokens.colorBrandForeground1, marginBottom: 20, animation: 'bounceIn 0.8s', filter: 'drop-shadow(0 2px 8px rgba(0,0,0,0.12))' }} />
        <div className={styles.title}>Elysian-Realm 大模型微调平台</div>
        <Text size={400} block className={styles.desc}>
          现代化、可视化的 LLM 微调与推理平台，支持 QLoRA、Optuna、ShareGPT 格式，<br />
          采用 Microsoft Fluent2 设计体系，极致流畅体验。
        </Text>
        <Text size={300} block className={styles.tip}>
          请选择上方标签页进入训练、推理、调参等功能。
        </Text>
      </div>
    </div>
  );
};

export default HomePage;
