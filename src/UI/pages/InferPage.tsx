import React from 'react';
import { Card, makeStyles, tokens, Subtitle1, Text, Input, Button } from '@fluentui/react-components';
import { Icon } from '@iconify/react';

const useStyles = makeStyles({
  card: {
    maxWidth: '700px',
    margin: '0 auto',
    padding: '32px',
    background: tokens.colorNeutralBackground2,
    boxShadow: tokens.shadow8,
    borderRadius: '16px',
    marginTop: '32px',
    animation: 'fadeIn 0.8s cubic-bezier(.4,0,.2,1)',
  },
  section: {
    marginBottom: '32px',
  },
  inputRow: {
    display: 'flex',
    gap: '16px',
    alignItems: 'center',
    marginBottom: '24px',
  },
  '@keyframes fadeIn': {
    from: { opacity: 0, transform: 'translateY(40px)' },
    to: { opacity: 1, transform: 'none' },
  },
});

const InferPage: React.FC = () => {
  const styles = useStyles();
  const [input, setInput] = React.useState('');
  const [output, setOutput] = React.useState('');

  return (
    <Card className={styles.card}>
      <Subtitle1>
        <Icon icon="fluent:chat-24-regular" style={{ marginRight: 8, color: tokens.colorBrandForeground1 }} />
        推理/对话
      </Subtitle1>
      <div className={styles.section}>
        <div className={styles.inputRow}>
          <Input
            placeholder="请输入对话内容"
            value={input}
            onChange={e => setInput(e.target.value)}
            style={{ flex: 1 }}
          />
          <Button
            appearance="primary"
            icon={<Icon icon="fluent:send-24-filled" />}
            onClick={() => setOutput('（这里显示模型回复，后端接入后自动填充）')}
          >
            发送
          </Button>
        </div>
        <Text block size={400} style={{ minHeight: 48, background: tokens.colorNeutralBackground3, borderRadius: 8, padding: 16 }}>
          {output || '回复内容将在此显示'}
        </Text>
      </div>
    </Card>
  );
};

export default InferPage;