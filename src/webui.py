# -*- coding: utf-8 -*-
# 文件: src/webui.py
# 功能: Gradio WebUI 主入口，支持训练、推理、调参等模式

import gradio as gr
import toml
import os

CONFIG_PATH = "config.toml"

def load_config():
    if not os.path.exists(CONFIG_PATH):
        # 默认配置
        cfg = {
            'train': {
                'learning_rate': 2e-5,
                'batch_size': 2,
                'num_train_epochs': 3,
                'lora_r': 8,
                'lora_alpha': 16,
                'lora_dropout': 0.1,
                'save_best': True
            },
            'infer': {
                'max_length': 128,
                'temperature': 1.0
            },
            'tune': {
                'n_trials': 10,
                'save_best': True
            }
        }
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            toml.dump(cfg, f)
        return cfg
    return toml.load(CONFIG_PATH)

def save_config(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        toml.dump(cfg, f)

def launch_webui():
    cfg = load_config()
    with gr.Blocks(title="Elysian-Realm WebUI") as demo:
        gr.Markdown("# 往事乐土 Elysian-Realm WebUI")
        with gr.Tab("训练"):
            use_optuna = gr.Checkbox(label="使用Optuna自动调参", value=cfg['train'].get('use_optuna', False))
            with gr.Row(visible=not cfg['train'].get('use_optuna', False)) as manual_params:
                lr = gr.Number(label="学习率", value=cfg['train']['learning_rate'])
                batch_size = gr.Number(label="Batch Size", value=cfg['train']['batch_size'])
                epochs = gr.Number(label="训练轮数", value=cfg['train']['num_train_epochs'])
                lora_r = gr.Number(label="LoRA r", value=cfg['train']['lora_r'])
                lora_alpha = gr.Number(label="LoRA alpha", value=cfg['train']['lora_alpha'])
                lora_dropout = gr.Number(label="LoRA Dropout", value=cfg['train']['lora_dropout'])
                grad_acc = gr.Number(label="梯度累积步数", value=cfg['train'].get('gradient_accumulation_steps', 4))
                fp16 = gr.Checkbox(label="使用FP16混合精度", value=cfg['train'].get('fp16', True))
                grad_ckpt = gr.Checkbox(label="梯度检查点", value=cfg['train'].get('gradient_checkpointing', True))
                dataloader_workers = gr.Number(label="数据加载线程数", value=cfg['train'].get('dataloader_num_workers', 2))
                seed = gr.Number(label="随机种子", value=cfg['train'].get('seed', 42))
                early_stop = gr.Number(label="EarlyStopping耐心", value=cfg['train'].get('early_stopping_patience', 5))
            with gr.Row(visible=cfg['train'].get('use_optuna', False)) as optuna_params:
                n_trials = gr.Number(label="Optuna实验轮数", value=cfg['tune']['n_trials'])
            save_best = gr.Checkbox(label="自动保存最优模型", value=cfg['train'].get('save_best', True))
            train_btn = gr.Button("开始训练")
            train_output = gr.Textbox(label="训练输出", lines=8)

            def toggle_params(use_optuna):
                return gr.update(visible=not use_optuna), gr.update(visible=use_optuna)
            use_optuna.change(toggle_params, [use_optuna], [manual_params, optuna_params])

            def on_train_click(
                use_optuna, lr, batch_size, epochs, lora_r, lora_alpha, lora_dropout, grad_acc, fp16, grad_ckpt, dataloader_workers, seed, early_stop, n_trials, save_best
            ):
                cfg['train']['use_optuna'] = use_optuna
                cfg['train']['learning_rate'] = lr
                cfg['train']['batch_size'] = batch_size
                cfg['train']['num_train_epochs'] = epochs
                cfg['train']['lora_r'] = lora_r
                cfg['train']['lora_alpha'] = lora_alpha
                cfg['train']['lora_dropout'] = lora_dropout
                cfg['train']['gradient_accumulation_steps'] = grad_acc
                cfg['train']['fp16'] = fp16
                cfg['train']['gradient_checkpointing'] = grad_ckpt
                cfg['train']['dataloader_num_workers'] = dataloader_workers
                cfg['train']['seed'] = seed
                cfg['train']['early_stopping_patience'] = early_stop
                cfg['train']['save_best'] = save_best
                cfg['tune']['n_trials'] = n_trials
                save_config(cfg)
                import subprocess
                if use_optuna:
                    # 调用tune_main
                    from src.tune import tune_main
                    tune_main()
                    return "已启动Optuna自动调参，日志请见控制台。"
                else:
                    from src.train import train_main
                    train_main(
                        learning_rate=lr,
                        per_device_train_batch_size=batch_size,
                        lora_r=lora_r,
                        lora_alpha=lora_alpha,
                        lora_dropout=lora_dropout,
                        num_train_epochs=epochs,
                        use_checkpoint=True,
                        save_best=save_best
                    )
                    return "训练已启动，日志请见控制台。"
            train_btn.click(
                on_train_click,
                [use_optuna, lr, batch_size, epochs, lora_r, lora_alpha, lora_dropout, grad_acc, fp16, grad_ckpt, dataloader_workers, seed, early_stop, n_trials, save_best],
                train_output
            )
        with gr.Tab("推理"):
            max_length = gr.Number(label="最大长度", value=cfg['infer']['max_length'])
            temperature = gr.Number(label="温度", value=cfg['infer']['temperature'])
            infer_input = gr.Textbox(label="输入内容")
            infer_btn = gr.Button("开始推理")
            infer_output = gr.Textbox(label="推理输出", lines=4)
            def on_infer_click(input_text, max_length, temperature):
                cfg['infer']['max_length'] = max_length
                cfg['infer']['temperature'] = temperature
                save_config(cfg)
                return "推理功能待实现..."
            infer_btn.click(on_infer_click, [infer_input, max_length, temperature], infer_output)
        with gr.Tab("调参"):
            n_trials = gr.Number(label="实验轮数", value=cfg['tune']['n_trials'])
            tune_save_best = gr.Checkbox(label="自动保存最优模型", value=cfg['tune']['save_best'])
            tune_btn = gr.Button("开始调参")
            tune_output = gr.Textbox(label="调参输出", lines=6)
            def on_tune_click(n_trials, save_best):
                cfg['tune']['n_trials'] = n_trials
                cfg['tune']['save_best'] = save_best
                save_config(cfg)
                return "调参功能待实现..."
            tune_btn.click(on_tune_click, [n_trials, tune_save_best], tune_output)
    demo.launch(server_port=7861)
