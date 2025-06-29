# -*- coding: utf-8 -*-
# 文件: src/train.py
# 功能: 微调大模型，集成数据增强、WandB日志、评估等

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
from opik import Experiment
import nlpaug.augmenter.word as naw
import torch

def train_main():
    """
    主训练入口，完成模型加载、数据增强、训练、保存等流程。
    """
    # 用OPIK初始化实验追踪，替换wandb
    experiment = Experiment(
        project="elysia-finetune",
        run_name="mistral-elysia"
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
        r=16,  # LoRA秩，越大表达能力越强，显存占用也越高
        lora_alpha=32,  # LoRA缩放系数
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],  # LoRA作用层
        lora_dropout=0.12,  # LoRA dropout防止过拟合
        bias="none",  # LoRA bias处理方式
        use_gradient_checkpointing=True,  # 是否启用梯度检查点
        random_state=3407,  # 随机种子
        max_seq_length=32768,  # 最大序列长度
        use_rslora=False,  # 是否使用rslora
        loftq_config=None,  # loftq配置
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
    # 修正：确保"conversations"字段存在
    if "conversations" in train_dataset.features:
        train_dataset = train_dataset.map(lambda x: {"text": [aug.augment(t) for t in x["text"]]}, batched=True, num_proc=1)
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
        output_dir="./results",  # 训练结果保存目录
        restore_callback_states_from_checkpoint=True,  # 是否从checkpoint恢复回调状态
        save_strategy="steps",  # 保存策略，可选"steps"或"epoch"
        save_steps=500,  # 每多少步保存一次
        save_total_limit=2,  # 最多保留多少个checkpoint
        save_safetensors=True,  # 是否保存为safetensors格式
        remove_unused_columns=False,  # 是否移除未用列
        num_train_epochs=7,  # 训练轮数
        per_device_train_batch_size=4,  # 单卡batch size
        gradient_accumulation_steps=4,  # 梯度累积步数
        learning_rate=2e-5,  # 学习率
        optim="adamw_torch",  # 优化器类型
        fp16=not torch.cuda.is_bf16_supported(),  # 是否使用fp16
        bf16=torch.cuda.is_bf16_supported(),  # 是否使用bf16
        max_grad_norm=0.3,  # 梯度裁剪
        dataloader_num_workers=2,  # dataloader线程数
        dataloader_persistent_workers=False,  # 是否持久化worker
        gradient_checkpointing=True,  # 是否启用梯度检查点
        dataloader_pin_memory=True,  # 是否pin memory
        warmup_ratio=0.1,  # 学习率预热比例
        logging_dir="./logs",  # 日志目录
        logging_steps=5,  # 日志记录步数
        per_device_eval_batch_size=8,  # 验证集batch size
        eval_strategy="steps",  # 验证策略
        eval_steps=25,  # 验证步数
        metric_for_best_model="eval_loss",  # 最佳模型指标
        load_best_model_at_end=True,  # 是否训练结束加载最佳模型
        report_to="tensorboard",  # 日志报告方式
    )
    tensorboard_callback = TensorBoardCallback()
    early_stopping_callback = EarlyStoppingCallback(early_stopping_patience=5)  # 早停容忍步数
    trainer = SFTTrainer(
        eval_dataset=eval_dataset.select(range(min(100, len(eval_dataset)))),
        max_eval_samples=min(100, len(eval_dataset)),
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        compute_metrics=compute_metrics,
        callbacks=[tensorboard_callback, early_stopping_callback, MemoryMonitorCallback()],
        save_strategy="steps",
        save_steps=500,
        max_seq_length=32768,
        tokenizer=tokenizer,
        output_dir=os.path.abspath("./results").replace("\\", "/"),
        formatting_func=lambda x: formatting_prompts_func(x, tokenizer),
        data_collator=data_collator,
    )
    torch.cuda.empty_cache()
    trainer.train()
    # 记录最终模型保存
    experiment.log_artifact("./elysia_model", artifact_type="model")
    experiment.end()
    model.save_pretrained("./elysia_adapter")
    tokenizer.save_pretrained("./elysia_adapter")
    model = model.merge_and_unload()
    model.save_pretrained("./elysia_model", safe_serialization=True)
    tokenizer.save_pretrained("./elysia_model")
