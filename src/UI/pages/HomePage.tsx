import React from 'react';
import { Card, makeStyles, tokens, Text, Subtitle1 } from '@fluentui/react-components';
import { Icon } from '@iconify/react';

const useStyles = makeStyles({
  card: {
    maxWidth: '600px',
    margin: '0 auto',
    padding: '32px',
    background: tokens.colorNeutralBackground2,
    boxShadow: tokens.shadow8,
    borderRadius: '16px',
    marginTop: '48px',
    textAlign: 'center',
    animation: 'fadeIn 0.8s cubic-bezier(.4,0,.2,1)',
  },
  icon: {
    fontSize: '48px',
    color: tokens.colorBrandForeground1,
    marginBottom: '16px',
    animation: 'bounceIn 0.8s',
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

const HomePage: React.FC = () => {
  const styles = useStyles();
  return (
    <Card className={styles.card}>
      <Icon icon="fluent:rocket-24-filled" className={styles.icon} />
      <Subtitle1>Elysian-Realm 大模型微调平台</Subtitle1>
      <Text size={400} block>
        现代化、可视化的 LLM 微调与推理平台，支持 QLoRA、Optuna、ShareGPT 格式，<br />
        采用 Microsoft Fluent2 设计体系，极致流畅体验。
      </Text>
      <Text size={300} block style={{ marginTop: 24, color: tokens.colorNeutralForeground3 }}>
        请选择上方标签页进入训练、推理、调参等功能。
      </Text>
    </Card>
  );
};

export default HomePage;
