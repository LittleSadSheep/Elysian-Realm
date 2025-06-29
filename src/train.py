# -*- coding: utf-8 -*-
# 文件: src/train.py
# 功能: 微调大模型，集成数据增强、Comet ML日志、评估等

from comet_ml import Experiment  # 必须放在所有深度学习相关import之前

# ========== Unsloth 必须在 transformers 之前导入 ==========
import os
import unsloth  # 必须最先导入
from unsloth import FastLanguageModel

# 其余 import 保持原样，FastLanguageModel 只需保留一次
from transformers import TrainingArguments, BitsAndBytesConfig, DataCollatorForLanguageModeling
from transformers.integrations import TensorBoardCallback
from transformers import EarlyStoppingCallback
from datasets import load_dataset
from unsloth.chat_templates import get_chat_template, standardize_sharegpt
from trl import SFTTrainer
from src.utils import formatting_prompts_func, compute_metrics, MemoryMonitorCallback

import nlpaug.augmenter.word as naw
import torch
import optuna  # 新增

def train_main(
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    lora_r=16,
    lora_alpha=32,
    lora_dropout=0.12,
    num_train_epochs=7,
    trial=None  # 用于optuna
):
    """
    主训练入口，完成模型加载、数据增强、训练、保存等流程。
    支持超参数传入，便于optuna自动调优。
    """
    # 用Comet.ml初始化实验追踪
    experiment = Experiment(
        project_name="elysia-finetune",
        workspace=None,  # 可指定你的comet workspace
        auto_output_logging="simple"
    )
    model_name = "unsloth/mistral-7b-instruct-v0.3-bnb-4bit"  # 可更换为其它模型
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,  # 是否启用4bit量化
        bnb_4bit_use_double_quant=True,  # 是否启用双重量化
        bnb_4bit_quant_type="nf4",  # 量化类型，可选"nf4"或"fp4"
        bnb_4bit_compute_dtype=torch.bfloat16  # 计算精度，可选torch.float16/torch.bfloat16
    )
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name,
        max_seq_length=32768,  # 最大序列长度
        dtype=torch.bfloat16,  # 加载精度
        token=None,
        device_map="auto",  # 自动分配设备
        quantization_config=bnb_config,
    )
    tokenizer = get_chat_template(tokenizer, chat_template="mistral")  # 可选其它模板
    model = FastLanguageModel.get_peft_model(
        model,
        r=lora_r,
        lora_alpha=lora_alpha,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_dropout=lora_dropout,
        bias="none",
        use_gradient_checkpointing=True,
        random_state=3407,
        max_seq_length=32768,
        use_rslora=False,
        loftq_config=None,
    )
    dataset = load_dataset(
        path="e:/Codes/Python/Elysian-Realm",  # 数据集路径
        data_files="data.json"  # 数据文件名
    )["train"]
    dataset = dataset.train_test_split(test_size=0.1, seed=42)  # 验证集比例和随机种子
    train_dataset = standardize_sharegpt(dataset["train"])
    eval_dataset = standardize_sharegpt(dataset["test"])
    # 数据增强
    aug = naw.SynonymAug(aug_src='wordnet')  # 可选其它增强方式
    # 修正：增强应针对 conversations 字段而不是 text 字段
    if "conversations" in train_dataset.features:
        def augment_conversations(batch):
            # 对每条对话的每个 value 字段做增强
            for convo in batch["conversations"]:
                for msg in convo:
                    if "value" in msg and isinstance(msg["value"], str):
                        msg["value"] = aug.augment(msg["value"])
            return batch
        train_dataset = train_dataset.map(augment_conversations, batched=True, num_proc=1)
        train_dataset = train_dataset.map(lambda x: formatting_prompts_func(x, tokenizer), batched=True, num_proc=1)
    else:
        train_dataset = train_dataset.map(lambda x: formatting_prompts_func(x, tokenizer), batched=True, num_proc=1)
    eval_dataset = eval_dataset.map(lambda x: formatting_prompts_func(x, tokenizer), batched=True, num_proc=1)
    print(f"训练集样本数: {len(train_dataset)}")
    print(f"验证集样本数: {len(eval_dataset)}")
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False,  # 是否使用MLM
        pad_to_multiple_of=8  # 填充到8的倍数
    )
    training_args = TrainingArguments(
        output_dir="./results",
        restore_callback_states_from_checkpoint=True,
        save_strategy="steps",
        save_steps=500,
        save_total_limit=2,
        save_safetensors=True,
        remove_unused_columns=False,
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=per_device_train_batch_size,
        gradient_accumulation_steps=4,
        learning_rate=learning_rate,
        optim="adamw_torch",
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        max_grad_norm=0.3,
        dataloader_num_workers=2,
        dataloader_persistent_workers=False,
        gradient_checkpointing=True,
        dataloader_pin_memory=True,
        warmup_ratio=0.1,
        logging_dir="./logs",
        logging_steps=5,
        per_device_eval_batch_size=8,
        eval_strategy="steps",
        eval_steps=25,
        metric_for_best_model="eval_loss",
        load_best_model_at_end=True,
        report_to="tensorboard",
    )
    tensorboard_callback = TensorBoardCallback()
    early_stopping_callback = EarlyStoppingCallback(early_stopping_patience=5)  # 早停容忍步数
    # 初始化并运行训练器
    try:
        # 修复Unsloth/TRL metrics文件编码问题（强制utf-8）
        import builtins
        _original_open = builtins.open
        def custom_open(file, mode='r', encoding='utf-8', errors='ignore', **kwargs):
            if 'b' in mode:
                return _original_open(file, mode=mode, **kwargs)
            else:
                return _original_open(file, mode=mode, encoding=encoding, errors=errors, **kwargs)
        builtins.open = custom_open
        trainer = SFTTrainer(
            eval_dataset=eval_dataset.select(range(min(100, len(eval_dataset)))),  # 自动适配数据量
            max_eval_samples=min(100, len(eval_dataset)),  # 自动适配数据量
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            compute_metrics=compute_metrics,
            callbacks=[tensorboard_callback, early_stopping_callback, MemoryMonitorCallback()],
            save_strategy="steps",
            save_steps=500,
            max_seq_length=32768,  # 保持一致
            tokenizer=tokenizer,
            output_dir=os.path.abspath("./results").replace("\\", "/"),
            formatting_func=formatting_prompts_func,  # 修正：传入函数而不是字符串
            data_collator=data_collator,
        )
    except FileNotFoundError as e:
        print(f"Unsloth/TRL metrics文件缺失或损坏，报错信息：{e}")
        print("请尝试重新安装unsloth和trl，或清理unsloth_compiled_cache目录后重试。")
        print("命令示例：\npip install --upgrade --force-reinstall unsloth trl\n或删除unsloth_compiled_cache文件夹。")
        raise
    torch.cuda.empty_cache()
    trainer.train()
    # 记录最终模型保存
    experiment.log_model("elysia_model", "./elysia_model")
    experiment.end()
    model.save_pretrained("./elysia_adapter")
    tokenizer.save_pretrained("./elysia_adapter")
    model = model.merge_and_unload()
    model.save_pretrained("./elysia_model", safe_serialization=True)
    tokenizer.save_pretrained("./elysia_model")
    tokenizer.save_pretrained("./elysia_model")

    # 如果是optuna调优，返回验证损失
    if trial is not None:
        eval_metrics = trainer.evaluate()
        return eval_metrics.get("eval_loss", None)

# 新增Optuna调优入口
def tune_main():
    """
    Optuna自动调参入口
    """
    def objective(trial):
        # 搜索空间
        learning_rate = trial.suggest_loguniform("learning_rate", 1e-6, 5e-4)
        per_device_train_batch_size = trial.suggest_categorical("per_device_train_batch_size", [2, 4, 8])
        lora_r = trial.suggest_categorical("lora_r", [8, 16, 32])
        lora_alpha = trial.suggest_categorical("lora_alpha", [16, 32, 64])
        lora_dropout = trial.suggest_uniform("lora_dropout", 0.05, 0.3)
        num_train_epochs = trial.suggest_int("num_train_epochs", 3, 10)
        # 调用train_main并返回验证损失
        return train_main(
            learning_rate=learning_rate,
            per_device_train_batch_size=per_device_train_batch_size,
            lora_r=lora_r,
            lora_alpha=lora_alpha,
            lora_dropout=lora_dropout,
            num_train_epochs=num_train_epochs,
            trial=trial
        )
    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=10)
