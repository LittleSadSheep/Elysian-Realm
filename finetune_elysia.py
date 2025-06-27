import sys
import io
import os
import builtins
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
# 导入Unsloth的FastLanguageModel，用于高效加载和训练模型，影响模型加载速度和GPU内存使用
from unsloth import FastLanguageModel
# 导入数据集加载工具，用于加载训练数据，影响CPU内存使用（数据加载阶段）
from datasets import load_dataset
# 导入分词器、训练参数配置和量化配置工具，影响模型预处理和训练过程
from transformers import AutoTokenizer, TrainingArguments, BitsAndBytesConfig
# 导入SFTTrainer，用于监督微调，影响训练流程和模型性能
from trl import SFTTrainer
import torch  # 导入PyTorch，深度学习框架，影响GPU使用和计算效率
from datasets import load_dataset  # 确保导入 load_dataset
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, DataCollatorForLanguageModeling, BitsAndBytesConfig
from unsloth import FastLanguageModel
from trl import SFTTrainer
import torch

# 重写open函数强制使用utf-8编码，避免文件读取时的编码错误，对性能无直接影响
_original_open = builtins.open
def custom_open(file, mode='r', encoding='utf-8', errors='ignore', **kwargs):
    if 'b' in mode:  # 二进制模式不修改编码
        return _original_open(file, mode=mode, **kwargs)
    else:  # 文本模式强制使用utf-8编码
        return _original_open(file, mode=mode, encoding=encoding, errors=errors, **kwargs)
builtins.open = custom_open  # 替换内置open函数

def main():
    # 加载模型和分词器
    # 模型名称/路径，选择4bit量化版本以减少GPU内存占用，直接影响模型性能和GPU内存使用
    model_name = "unsloth/mistral-7b-instruct-v0.3-bnb-4bit"
    # 配置4bit量化参数，显著降低GPU内存使用（约节省75%显存），对模型精度影响较小
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,  # 启用4bit量化，核心参数，决定是否使用量化
        bnb_4bit_use_double_quant=True,  # 启用双重量化，进一步减少显存占用约0.4bit/参数
        bnb_4bit_quant_type="nf4",  # 使用NF4量化类型，专为LLM优化，精度高于普通4bit
        bnb_4bit_compute_dtype=torch.bfloat16  # 计算时使用bfloat16精度，平衡速度和精度
    )
    # 从预训练模型加载并应用量化配置，影响模型加载速度和初始GPU内存占用
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name,  # 指定模型名称/路径
        max_seq_length = 2048,  # 最大序列长度，影响GPU内存使用（更长序列需更多显存）和模型上下文理解能力
        dtype = torch.bfloat16,  # 模型数据类型，bfloat16比float32节省一半显存，对精度影响小
        token = None,  # Hugging Face访问令牌，无令牌时为None，不影响性能
        device_map = "auto",  # 自动分配设备（CPU/GPU），优化GPU内存使用
        quantization_config = bnb_config,  # 应用前面定义的量化配置
    )
    # 加载分词器，用于文本预处理，影响CPU内存使用（较小）
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    # 设置填充令牌为结束令牌，影响模型输入格式和训练稳定性
    tokenizer.pad_token = tokenizer.eos_token

    # 定义 LoRA 配置，影响模型微调效率和参数更新
    model = FastLanguageModel.get_peft_model(
        model,  # 基础模型
        r=8,  # LoRA注意力维度，影响模型微调能力和参数数量（r越大能力越强但参数越多）
        # 指定LoRA应用的目标模块，影响模型微调效果和GPU内存使用
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                       "gate_proj", "up_proj", "down_proj"],
        lora_alpha=32,  # LoRA缩放参数，与r共同决定更新强度（alpha/r为学习率缩放因子）
        lora_dropout=0.05,  # LoRA dropout率，防止过拟合，对模型泛化能力有影响
        bias="none",  # 是否训练偏置参数，"none"表示不训练，减少参数数量和显存使用
        use_gradient_checkpointing=True,  # 启用梯度检查点，节省GPU显存（约50%）但训练速度降低10-20%
        random_state=3407,  # 随机种子，保证训练可复现性，对性能无影响
        max_seq_length=2048,  # 最大序列长度，需与前面保持一致
        use_rslora=False,  # 禁用RS-LoRA，启用会改变LoRA更新方式，对性能影响因任务而异
        loftq_config=None,  # 禁用LoftQ量化，启用会进一步降低显存但可能影响精度
    )

    # 加载数据集，影响CPU内存使用（数据量越大占用越多）和训练时间
    dataset = load_dataset("text", data_files={"train": "training_data.txt"}, encoding="utf-8")["train"]
    # 分割训练集和验证集（10%数据用于验证）
    dataset = dataset.train_test_split(test_size=0.1, seed=42)
    train_dataset = dataset["train"]
    eval_dataset = dataset["test"]

    # 设置训练参数，全面影响训练速度、模型性能和资源使用
    training_args = TrainingArguments(
        output_dir="./results",  # 训练结果保存目录，对性能无影响

        resume_from_checkpoint=True,  # 启用检查点续传，不影响性能但影响训练连续性
        save_strategy="steps",  # 按步数保存检查点，影响磁盘I/O和训练中断恢复能力
        save_steps=500,  # 每500步保存一次，频繁保存增加磁盘I/O但降低中断风险
        save_total_limit=3,  # 最多保留3个检查点，影响磁盘空间占用

        num_train_epochs=4,  # 训练轮数，影响训练总时间和模型收敛程度（轮数越多可能过拟合）
        per_device_train_batch_size=26,  # 每个设备的批大小，影响GPU内存使用（越大占用越多）和训练速度（越大越快）
        gradient_accumulation_steps=1,  # 梯度累积步数，1表示不累积，增大可模拟大批次但不增加显存使用
        learning_rate=5e-5,  # 学习率，影响模型收敛速度和最终性能（过大可能不收敛，过小收敛慢）
        # 根据GPU是否支持bfloat16选择精度，影响GPU内存使用和计算速度
        fp16 = not torch.cuda.is_bf16_supported(),
        bf16 = torch.cuda.is_bf16_supported(),
        max_grad_norm = 0.3,  # 梯度裁剪阈值，防止梯度爆炸，影响训练稳定性
        dataloader_num_workers = 8,  # 数据加载进程数，影响CPU内存使用和数据加载速度（过多可能占用大量CPU）
        dataloader_persistent_workers = True,  # 保持数据加载进程，减少重复初始化开销，加快训练速度
        dataloader_pin_memory = True,  # 固定内存到GPU，加速数据传输，影响GPU内存使用（微小）
        warmup_ratio = 0.03,  # 学习率预热比例，3%步数用于预热，影响模型收敛稳定性
        logging_dir="./logs",  # 日志保存目录，对性能无影响
        logging_steps=50,  # 每50步记录一次日志，影响磁盘I/O（微小）
        optim="adamw_torch",  # 使用标准优化器减少内存碎片化，提升计算效率
        # optim="paged_adamw_8bit"  # 使用8bit分页优化器，显著节省GPU内存（约50%），训练速度略有降低
        # 新增评估配置
        eval_strategy="steps",  # 按步数进行评估（原evaluation_strategy已重命名）
        eval_steps=500,  # 每500步评估一次
        metric_for_best_model="eval_loss",  # 以验证损失作为最佳模型指标
        load_best_model_at_end=True,  # 训练结束时加载最佳模型

        report_to="tensorboard",  # 启用TensorBoard可视化
    )

    # 添加TensorBoard回调
    from transformers.integrations import TensorBoardCallback
    from transformers import EarlyStoppingCallback
    tensorboard_callback = TensorBoardCallback()

    # 定义评估指标计算函数（困惑度）
    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        loss = torch.nn.functional.cross_entropy(
            logits.view(-1, logits.size(-1)), 
            labels.view(-1),
            ignore_index=-100  # 忽略填充标记
        )
        perplexity = torch.exp(loss).item()  # 困惑度=exp(loss)
        return {"perplexity": perplexity, "eval_loss": loss.item()}

    # 导入检查点工具，用于恢复训练
    from transformers.trainer_utils import get_last_checkpoint
    # 获取最后一个检查点路径，影响训练恢复能力
    last_checkpoint = get_last_checkpoint("./results")
    if last_checkpoint is not None:
        print(f"""

=== 发现历史检查点 {last_checkpoint}，自动恢复训练 ===

""")

    # 初始化并运行训练器
    trainer = SFTTrainer(
        model=model,  # 待训练模型

        args=training_args,  # 训练参数配置
        train_dataset=train_dataset,  # 训练数据集
        eval_dataset=eval_dataset,  # 验证数据集
        compute_metrics=compute_metrics,  # 添加评估指标计算
        callbacks=[tensorboard_callback, EarlyStoppingCallback],  # 添加TensorBoard回调
        save_strategy="steps",
        save_steps=500,
        resume_from_checkpoint=last_checkpoint,  # 从检查点恢复
        max_seq_length=512,  # SFT训练的最大序列长度，覆盖前面的2048，影响GPU内存使用
        tokenizer=tokenizer,  # 分词器
    )
    try:
        trainer.train()  # 开始训练，核心步骤，占用主要GPU资源和训练时间
        # 训练结束后打印最佳评估指标
        print(f"最佳验证损失: {trainer.state.best_metric}")
        print(f"最佳困惑度: {torch.exp(torch.tensor(trainer.state.best_metric)).item()}")
    except KeyboardInterrupt:
        # 用户中断时保存检查点，保护训练进度，对性能无影响
        print("\nTraining interrupted by user. Saving current checkpoint...")
        trainer.save_model()  # 保存模型权重
        trainer.save_state()  # 保存训练状态
        model.save_pretrained("./elysia_model")  # 保存最终模型到指定目录
        print("Checkpoint saved successfully.")
        sys.exit(0)  # 退出程序

    # 训练完成后保存模型，影响磁盘空间使用
    model.save_pretrained("./elysia_model")

if __name__ == '__main__':
    import multiprocessing  # 多进程模块，用于Windows系统支持
    multiprocessing.freeze_support()  # 修复Windows下多进程问题，对性能无影响
    main()  # 执行主函数