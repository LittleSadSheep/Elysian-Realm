import React from 'react';
import { Card, makeStyles, tokens, Subtitle1, Text, Button, List, ListItem } from '@fluentui/react-components';
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
  modelList: {
    marginTop: '16px',
    marginBottom: '16px',
    background: tokens.colorNeutralBackground3,
    borderRadius: '8px',
    padding: '8px',
  },
  modelItem: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: '8px 0',
    borderBottom: `1px solid ${tokens.colorNeutralStroke3}`,
    ':last-child': { borderBottom: 'none' },
  },
  modelInfo: {
    display: 'flex',
    flexDirection: 'column',
  },
  modelName: {
    fontWeight: 500,
  },
  modelDesc: {
    color: tokens.colorNeutralForeground3,
    fontSize: '13px',
  },
  '@keyframes fadeIn': {
    from: { opacity: 0, transform: 'translateY(40px)' },
    to: { opacity: 1, transform: 'none' },
  },
});

const mockModels = [
  { name: 'elysia_model', desc: '主模型（合并LoRA）', time: '2025-06-30' },
  { name: 'elysia_adapter', desc: 'LoRA Adapter', time: '2025-06-29' },
  { name: 'output/best_model', desc: '最优模型', time: '2025-06-28' },
];

const ModelPage: React.FC = () => {
  const styles = useStyles();
  return (
    <Card className={styles.card}>
      <Subtitle1>
        <Icon icon="fluent:database-24-regular" style={{ marginRight: 8, color: tokens.colorBrandForeground1 }} />
        模型管理
      </Subtitle1>
      <div className={styles.section}>
        <Text size={400} block>
          管理、下载、删除本地模型文件。<br />
          （后端接入后可自动列出所有模型及操作）
        </Text>
        <List className={styles.modelList}>
          {mockModels.map(m => (
            <ListItem key={m.name} className={styles.modelItem}>
              <div className={styles.modelInfo}>
                <span className={styles.modelName}>{m.name}</span>
                <span className={styles.modelDesc}>{m.desc} | {m.time}</span>
              </div>
              <div>
                <Button appearance="subtle" icon={<Icon icon="fluent:download-24-regular" />} style={{ marginRight: 8 }} />
                <Button appearance="subtle" icon={<Icon icon="fluent:delete-24-regular" />} />
              </div>
            </ListItem>
          ))}
        </List>
      </div>
    </Card>
  );
};

export default ModelPage;
