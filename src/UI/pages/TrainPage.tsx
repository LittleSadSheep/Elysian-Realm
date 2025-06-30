import * as React from 'react';
import { Card, makeStyles, tokens, Text, Subtitle1, Button, Input, Switch, Dropdown, Option, ProgressBar } from '@fluentui/react-components';
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
  paramRow: {
    display: 'flex',
    gap: '16px',
    marginBottom: '16px',
    alignItems: 'center',
  },
  label: {
    minWidth: '120px',
    fontWeight: 500,
  },
  '@keyframes fadeIn': {
    from: { opacity: 0, transform: 'translateY(40px)' },
    to: { opacity: 1, transform: 'none' },
  },
});

const TrainPage: React.FC = () => {
  const styles = useStyles();
  const [useOptuna, setUseOptuna] = React.useState(false);
  const [saveBest, setSaveBest] = React.useState(true);
  // 训练参数状态
  const [params, setParams] = React.useState({
    learning_rate: 2e-5,
    batch_size: 2,
    num_train_epochs: 3,
    lora_r: 8,
    lora_alpha: 16,
    lora_dropout: 0.1,
    gradient_accumulation_steps: 4,
    fp16: true,
    gradient_checkpointing: true,
    dataloader_num_workers: 2,
    seed: 42,
    early_stopping_patience: 5,
    n_trials: 10,
  });
  // 动效：训练进度
  const [progress, setProgress] = React.useState(0);
  const [training, setTraining] = React.useState(false);

  return (
    <Card className={styles.card}>
      <div className={styles.section}>
        <Subtitle1>
          <Icon icon="fluent:play-circle-24-regular" style={{ marginRight: 8, color: tokens.colorBrandForeground1 }} />
          训练参数配置
        </Subtitle1>
        <div className={styles.paramRow}>
          <span className={styles.label}>使用Optuna自动调参</span>
          <Switch checked={useOptuna} onChange={(_, d) => setUseOptuna(d.checked)} />
        </div>
      </div>
      {!useOptuna && (
        <div className={styles.section}>
          <div className={styles.paramRow}>
            <span className={styles.label}>学习率</span>
            <Input type="number" value={String(params.learning_rate)} step={1e-6} onChange={e => setParams(p => ({ ...p, learning_rate: +e.target.value }))} />
            <span className={styles.label}>Batch Size</span>
            <Input type="number" value={String(params.batch_size)} min={1} max={16} onChange={e => setParams(p => ({ ...p, batch_size: +e.target.value }))} />
          </div>
          <div className={styles.paramRow}>
            <span className={styles.label}>训练轮数</span>
            <Input type="number" value={String(params.num_train_epochs)} min={1} max={20} onChange={e => setParams(p => ({ ...p, num_train_epochs: +e.target.value }))} />
            <span className={styles.label}>LoRA r</span>
            <Input type="number" value={String(params.lora_r)} min={1} max={64} onChange={e => setParams(p => ({ ...p, lora_r: +e.target.value }))} />
            <span className={styles.label}>LoRA alpha</span>
            <Input type="number" value={String(params.lora_alpha)} min={1} max={128} onChange={e => setParams(p => ({ ...p, lora_alpha: +e.target.value }))} />
          </div>
          <div className={styles.paramRow}>
            <span className={styles.label}>LoRA Dropout</span>
            <Input type="number" value={String(params.lora_dropout)} min={0} max={0.5} step={0.01} onChange={e => setParams(p => ({ ...p, lora_dropout: +e.target.value }))} />
            <span className={styles.label}>梯度累积步数</span>
            <Input type="number" value={String(params.gradient_accumulation_steps)} min={1} max={32} onChange={e => setParams(p => ({ ...p, gradient_accumulation_steps: +e.target.value }))} />
          </div>
          <div className={styles.paramRow}>
            <span className={styles.label}>FP16混合精度</span>
            <Switch checked={params.fp16} onChange={(_, d) => setParams(p => ({ ...p, fp16: d.checked }))} />
            <span className={styles.label}>梯度检查点</span>
            <Switch checked={params.gradient_checkpointing} onChange={(_, d) => setParams(p => ({ ...p, gradient_checkpointing: d.checked }))} />
            <span className={styles.label}>数据加载线程数</span>
            <Input type="number" value={String(params.dataloader_num_workers)} min={1} max={16} onChange={e => setParams(p => ({ ...p, dataloader_num_workers: +e.target.value }))} />
          </div>
          <div className={styles.paramRow}>
            <span className={styles.label}>随机种子</span>
            <Input type="number" value={String(params.seed)} min={0} max={99999} onChange={e => setParams(p => ({ ...p, seed: +e.target.value }))} />
            <span className={styles.label}>EarlyStopping耐心</span>
            <Input type="number" value={String(params.early_stopping_patience)} min={1} max={20} onChange={e => setParams(p => ({ ...p, early_stopping_patience: +e.target.value }))} />
          </div>
        </div>
      )}
      {useOptuna && (
        <div className={styles.section}>
          <div className={styles.paramRow}>
            <span className={styles.label}>Optuna实验轮数</span>
            <Input type="number" value={String(params.n_trials)} min={1} max={100} onChange={e => setParams(p => ({ ...p, n_trials: +e.target.value }))} />
          </div>
        </div>
      )}
      <div className={styles.section}>
        <div className={styles.paramRow}>
          <span className={styles.label}>自动保存最优模型</span>
          <Switch checked={saveBest} onChange={(_, d) => setSaveBest(d.checked)} />
        </div>
        <Button appearance="primary" icon={<Icon icon="fluent:play-24-filled" />} disabled={training}>
          {training ? '训练中...' : '开始训练'}
        </Button>
        {training && <ProgressBar value={progress} max={100} style={{ marginTop: 16 }} />}
      </div>
    </Card>
  );
};

export default TrainPage;
