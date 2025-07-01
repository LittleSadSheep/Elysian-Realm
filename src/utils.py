# -*- coding: utf-8 -*-
# 文件: src/utils.py
# 功能: 通用工具函数，包括数据格式化、评估指标、内存监控等

import torch
from sklearn.metrics import accuracy_score, recall_score, f1_score
from transformers import TrainerCallback
import psutil


def formatting_prompts_func(examples, tokenizer):
    """
    格式化ShareGPT对话为模型输入文本，并添加eos token
    """
    # tokenizer.eos_token 可根据模型实际情况调整
    convos = examples["conversations"]
    texts = [
        tokenizer.apply_chat_template(
            convo, tokenize=False, add_generation_prompt=False
        )
        + tokenizer.eos_token
        for convo in convos
    ]
    return {"text": texts}


def compute_metrics(eval_pred):
    """
    计算评估指标：困惑度、损失、准确率、召回率、F1
    """
    # zero_division=0 可调整为其它值以避免除零警告
    # average='macro' 可调整为'micro'或'weighted'等
    logits, labels = eval_pred
    if isinstance(logits, tuple):
        logits = logits[0]
    if not torch.is_tensor(logits):
        logits = torch.tensor(logits, dtype=torch.float32)
    if not torch.is_tensor(labels):
        labels = torch.tensor(labels, dtype=torch.long)
    if len(logits.shape) == 3:
        logits = logits.reshape(-1, logits.shape[-1])
    if len(labels.shape) == 2:
        labels = labels.reshape(-1)
    valid_indices = labels != -100
    logits = logits[valid_indices]
    labels = labels[valid_indices]
    if logits.numel() == 0 or labels.numel() == 0:
        # 防止空tensor导致报错
        return {
            "perplexity": float("nan"),
            "eval_loss": float("nan"),
            "accuracy": 0,
            "recall": 0,
            "f1": 0,
        }
    loss = torch.nn.functional.cross_entropy(logits, labels, ignore_index=-100)
    perplexity = torch.exp(loss).item()
    preds = torch.argmax(logits, dim=-1)
    acc = accuracy_score(labels.cpu().numpy(), preds.cpu().numpy())
    rec = recall_score(
        labels.cpu().numpy(), preds.cpu().numpy(), average="macro", zero_division=0
    )
    f1 = f1_score(
        labels.cpu().numpy(), preds.cpu().numpy(), average="macro", zero_division=0
    )
    return {
        "perplexity": perplexity,
        "eval_loss": loss.item(),
        "accuracy": acc,
        "recall": rec,
        "f1": f1,
    }


class MemoryMonitorCallback(TrainerCallback):
    """
    训练/评估时监控内存占用
    """

    def on_evaluate(self, args, state, control, **kwargs):
        process = psutil.Process()
        mem_info = process.memory_info()
        print(
            f"\n评估阶段内存使用：RSS={mem_info.rss // 1024 // 1024}MB, VMS={mem_info.vms // 1024 // 1024}MB"
        )
        torch.cuda.empty_cache()

    def on_prediction_step(self, args, state, control, **kwargs):
        torch.cuda.empty_cache()
