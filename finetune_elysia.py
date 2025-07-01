import os
import builtins
import sys
import torch  # 导入PyTorch，深度学习框架，影响GPU使用和计算效率
from datasets import load_dataset  # 保留这一行
from transformers import TrainingArguments, BitsAndBytesConfig
from unsloth import FastLanguageModel

# from unsloth import formatting_func  # 替换为此导入
from trl import SFTTrainer
from unsloth.chat_templates import get_chat_template
from unsloth.chat_templates import standardize_sharegpt

# __init__
interrupt_dir = None
last_checkpoint = None
gguf_dir = "./ggufs"
# checkpoint_path = None
# 重写open函数强制使用utf-8编码，避免文件读取时的编码错误，对性能无直接影响
_original_open = builtins.open


def custom_open(file, mode="r", encoding="utf-8", errors="ignore", **kwargs):
    if "b" in mode:  # 二进制模式不修改编码
        return _original_open(file, mode=mode, **kwargs)
    else:  # 文本模式强制使用utf-8编码
        return _original_open(
            file, mode=mode, encoding=encoding, errors=errors, **kwargs
        )


builtins.open = custom_open  # 替换内置open函数

# 在评估回调中添加
from transformers import TrainerCallback
import psutil


class MemoryMonitorCallback(TrainerCallback):
    def on_evaluate(self, args, state, control, **kwargs):
        process = psutil.Process()
        mem_info = process.memory_info()
        print(
            f"\n评估阶段内存使用：RSS={mem_info.rss // 1024 // 1024}MB, VMS={mem_info.vms // 1024 // 1024}MB"
        )
        torch.cuda.empty_cache()

    def on_prediction_step(self, args, state, control, **kwargs):
        torch.cuda.empty_cache()


def main():
    # 增强版检查点恢复逻辑
    from transformers.trainer_utils import get_last_checkpoint

    if os.path.exists("./results") and get_last_checkpoint("./results") is not None:
        try:
            global last_checkpoint
            last_checkpoint = get_last_checkpoint("./results").replace("\\", "/")

            required_files = [
                "training_args.bin",
                "optimizer.pt",
                "scheduler.pt",
                "trainer_state.json",
                "rng_state.pth",
                "adapter_config.json",
                "adapter_model.safetensors",
            ]
            if last_checkpoint:
                # 统一检查点路径格式
                # global checkpoint_path
                # checkpoint_path = last_checkpoint.replace("\\", "/")
                missing = [
                    f
                    for f in required_files
                    if not os.path.isfile(os.path.join(last_checkpoint, f))
                ]
                if missing:
                    print(
                        f"\n⚠️ 发现不完整检查点 {last_checkpoint}, 缺失文件: {', '.join(missing)}"
                    )

                else:
                    print(f"\n✅ 找到有效检查点: {last_checkpoint}")
        except Exception as e:
            print(f"\n⚠️ 检查点恢复异常: {str(e)}")

    # 加载模型和分词器
    # 模型名称/路径，选择4bit量化版本以减少GPU内存占用，直接影响模型性能和GPU内存使用
    model_name = "unsloth/mistral-7b-instruct-v0.3-bnb-4bit"
    # 配置4bit量化参数，显著降低GPU内存使用（约节省75%显存），对模型精度影响较小
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,  # 启用4bit量化，核心参数，决定是否使用量化
        bnb_4bit_use_double_quant=True,  # 启用双重量化，进一步减少显存占用约0.4bit/参数
        bnb_4bit_quant_type="nf4",  # 使用NF4量化类型，专为LLM优化，精度高于普通4bit
        bnb_4bit_compute_dtype=torch.bfloat16,  # 计算时使用bfloat16精度，平衡速度和精度
    )
    # 从预训练模型加载并应用量化配置，影响模型加载速度和初始GPU内存占用
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name,
        max_seq_length=32768,  # 降低序列长度
        dtype=torch.bfloat16,
        token=None,
        device_map="auto",
        quantization_config=bnb_config,
    )
    tokenizer = get_chat_template(
        tokenizer,
        chat_template="mistral",
    )

    def formatting_prompts_func(examples):
        convos = examples["conversations"]
        texts = [
            tokenizer.apply_chat_template(
                convo, tokenize=False, add_generation_prompt=False
            )
            for convo in convos
        ]
        return {
            "text": texts,
        }

    tokenizer.pad_token = tokenizer.eos_token

    # 定义 LoRA 配置，影响模型微调效率和参数更新
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,  # 增大LoRA维度
        lora_alpha=32,  # 增大LoRA缩放
        target_modules=[
            "q_proj",
            "k_proj",
            "v_proj",
            "o_proj",
            "gate_proj",
            "up_proj",
            "down_proj",
        ],
        lora_dropout=0.12,  # 建议0.1~0.3，防止过拟合
        bias="none",
        use_gradient_checkpointing=True,
        random_state=3407,
        max_seq_length=32768,
        use_rslora=False,
        loftq_config=None,
    )

    # 加载ShareGPT格式数据集
    dataset = load_dataset(
        path="e:/Codes/Python/Elysian-Realm",  # 指向包含data.json和dataset_info.json的目录
        data_files="data.json",
    )["train"]

    # 分割训练集和验证集（10%数据用于验证）
    dataset = dataset.train_test_split(test_size=0.1, seed=42)
    train_dataset = dataset["train"]
    eval_dataset = dataset["test"]

    # 分别标准化和格式化
    train_dataset = standardize_sharegpt(train_dataset)
    eval_dataset = standardize_sharegpt(eval_dataset)
    # 强制单进程，避免Windows多进程序列化问题
    train_dataset = train_dataset.map(formatting_prompts_func, batched=True, num_proc=1)
    eval_dataset = eval_dataset.map(formatting_prompts_func, batched=True, num_proc=1)

    # 打印数据集大小，便于调试
    print(f"训练集样本数: {len(train_dataset)}")
    print(f"验证集样本数: {len(eval_dataset)}")

    # 设置训练参数，全面影响训练速度、模型性能和资源使用
    training_args = TrainingArguments(
        output_dir="./results",  # 训练结果保存目录，对性能无影响
        restore_callback_states_from_checkpoint=True,
        save_strategy="steps",
        save_steps=500,
        save_total_limit=2,  # 限制为2个最新检查点
        save_safetensors=True,
        remove_unused_columns=False,
        num_train_epochs=7,  # 增大轮数
        per_device_train_batch_size=4,  # 增大batch size
        gradient_accumulation_steps=4,  # 配合batch size，适当累积
        learning_rate=2e-5,  # 更小学习率 1e-5
        optim="adamw_torch",
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        max_grad_norm=0.3,
        dataloader_num_workers=2,  # 评估阶段进一步减少worker
        # prefetch_factor = 1,  # 降低预取批次数量
        dataloader_persistent_workers=False,  # 禁用持久worker释放内存
        gradient_checkpointing=True,  # 启用梯度检查点
        dataloader_pin_memory=True,  # 固定内存到GPU，加速数据传输，影响GPU内存使用（微小）
        warmup_ratio=0.1,  # 学习率预热比例，3%步数用于预热，影响模型收敛稳定性
        logging_dir="./logs",  # 日志保存目录，对性能无影响
        logging_steps=5,  # 每50步记录一次日志，影响磁盘I/O（微小）
        # optim="adamw_torch",  # 使用标准优化器减少内存碎片化，提升计算效率
        # optim="paged_adamw_8bit"  # 使用8bit分页优化器，显著节省GPU内存（约50%），训练速度略有降低
        # 新增评估批次参数
        per_device_eval_batch_size=8,
        eval_strategy="steps",  # 按步数进行评估（原evaluation_strategy已重命名）
        eval_steps=25,  # 每500步评估一次
        metric_for_best_model="eval_loss",  # 以验证损失作为最佳模型指标
        load_best_model_at_end=True,  # 训练结束时加载最佳模型
        report_to="tensorboard",  # 启用TensorBoard可视化
    )

    # 添加TensorBoard回调
    from transformers.integrations import TensorBoardCallback
    from transformers import EarlyStoppingCallback

    tensorboard_callback = TensorBoardCallback()
    early_stopping_callback = EarlyStoppingCallback(early_stopping_patience=5)  # 更稳健

    # 定义评估指标计算函数（困惑度）
    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        # 处理可能的元组输出
        if isinstance(logits, tuple):
            logits = logits[0]

        # 转换numpy数组为tensor
        if not torch.is_tensor(logits):
            logits = torch.tensor(logits, dtype=torch.float32)
        if not torch.is_tensor(labels):
            labels = torch.tensor(labels, dtype=torch.long)

        # 确保维度匹配
        if len(logits.shape) == 3:
            logits = logits.reshape(-1, logits.shape[-1])
        if len(labels.shape) == 2:
            labels = labels.reshape(-1)

        # 过滤无效标签
        valid_indices = labels != -100
        logits = logits[valid_indices]
        labels = labels[valid_indices]

        # 计算损失和困惑度
        loss = torch.nn.functional.cross_entropy(logits, labels, ignore_index=-100)
        perplexity = torch.exp(loss).item()
        return {"perplexity": perplexity, "eval_loss": loss.item()}

    # 导入检查点工具，用于恢复训练
    from transformers.trainer_utils import get_last_checkpoint  # 显式导入
    # 获取最后一个检查点路径，影响训练恢复能力
    # 增强版检查点恢复

    # if os.path.exists("./results"):
    #     try:
    #         last_checkpoint = get_last_checkpoint("./results").replace("\\", "/")
    #         if last_checkpoint and not os.path.exists(os.path.join(last_checkpoint, "training_args.bin")):
    #             print(f"\n发现不完整检查点 {last_checkpoint}, 跳过恢复...")

    #     except Exception as e:
    #         print(f"\n检查点恢复失败: {str(e)}")

    if last_checkpoint:
        try:
            # 验证检查点完整性
            missing = [
                f
                for f in required_files
                if not os.path.exists(os.path.join(last_checkpoint, f))
            ]
            if not missing:
                print(f"成功加载检查点: {last_checkpoint}")
            else:
                print(f"缺失文件: {', '.join(missing)}")

        except Exception as e:
            print(f"检查点验证异常: {str(e)}")
        print(
            f"\n找到有效检查点 {last_checkpoint}\n包含文件: {', '.join(os.listdir(last_checkpoint))}\n"
        )
    else:
        print("\n未找到有效检查点，开始全新训练\n")

    # 初始化并运行训练器
    trainer = SFTTrainer(
        eval_dataset=eval_dataset.select(
            range(min(100, len(eval_dataset)))
        ),  # 自动适配数据量
        max_eval_samples=min(100, len(eval_dataset)),  # 自动适配数据量
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        compute_metrics=compute_metrics,
        callbacks=[tensorboard_callback, early_stopping_callback],
        save_strategy="steps",
        save_steps=500,
        max_seq_length=32768,  # 保持一致
        tokenizer=tokenizer,
        output_dir=os.path.abspath("./results").replace("\\", "/"),
        formatting_func=formatting_prompts_func,  # 修正：传入函数而不是字符串
    )

    # 训练前清空缓存
    torch.cuda.empty_cache()
    try:
        if last_checkpoint:
            trainer.train(resume_from_checkpoint=last_checkpoint)  # 显式传递
        else:
            trainer.train()
        # 训练结束后打印最佳评估指标
        print(f"最佳验证损失: {trainer.state.best_metric}")
        print(
            f"最佳困惑度: {torch.exp(torch.tensor(trainer.state.best_metric)).item()}"
        )
        # model.save_pretrained_gguf(gguf_dir, tokenizer, quantization_method = "q4_k_m")
    except KeyboardInterrupt:
        # 创建独立的中断检查点目录
        global interrupt_dir
        interrupt_dir = os.path.abspath(
            os.path.join("results", f"checkpoint-{trainer.state.global_step}")
        ).replace("\\", "/")
        os.makedirs(interrupt_dir, exist_ok=True)
        os.makedirs(interrupt_dir, exist_ok=True)

        print(f"\n⚠️ 用户中断训练，正在保存检查点到 {interrupt_dir}...")

        # 保存完整检查点
        # 显式保存完整模型配置
        trainer.model.save_pretrained(
            interrupt_dir, safe_serialization=True, max_shard_size="2GB"
        )
        # 保存QLoRA适配器配置
        trainer.model.peft_config["default"].save_pretrained(
            os.path.join(interrupt_dir, "adapter_config")
        )
        # 统一路径处理

        interrupt_dir = os.path.abspath(interrupt_dir).replace("\\", "/")
        # 保存QLoRA适配器配置
        trainer.model.peft_config["default"].save_pretrained(interrupt_dir)
        trainer.save_model(interrupt_dir)
        trainer._save_checkpoint(trainer.model, trial=None)
        trainer.save_model(interrupt_dir)
        trainer.save_state()

        # 保存完整状态并释放资源
        torch.cuda.empty_cache()
        with open(os.path.join(interrupt_dir, "interrupt_info.txt"), "w") as f:
            f.write(f"Interrupted at step {trainer.state.global_step}\n")
            f.write(f"Current_epoch: {trainer.state.epoch}\n")
            last_log = (
                trainer.state.log_history[-1] if trainer.state.log_history else {}
            )
            loss_val = last_log.get("loss") or last_log.get("eval_loss") or "N/A"
            f.write(f"Current_loss: {loss_val}")
        print(f"✅ 检查点已保存到 {interrupt_dir}")
        sys.exit(0)

    # 训练完成后保存模型，影响磁盘空间使用
    # model.save_pretrained("./elysia_model")
    # 训练完成后保存LoRA adapter
    model.save_pretrained("./elysia_adapter")
    tokenizer.save_pretrained("./elysia_adapter")
    # 合并LoRA权重并保存完整模型
    model = model.merge_and_unload()
    model.save_pretrained("./elysia_model", safe_serialization=True)
    tokenizer.save_pretrained("./elysia_model")

    # 训练前优化数据加载
    if hasattr(trainer, "get_train_dataloader"):
        trainer.get_train_dataloader().prefetch_factor = 1
    if (
        hasattr(trainer, "get_eval_dataloader")
        and trainer.get_eval_dataloader() is not None
    ):
        trainer.get_eval_dataloader().prefetch_factor = 1  # 评估集


if __name__ == "__main__":
    import multiprocessing  # 多进程模块，用于Windows系统支持

    multiprocessing.freeze_support()  # 修复Windows下多进程问题，对性能无影响
    main()  # 执行主函数
