from transformers import AutoTokenizer
from unsloth import FastLanguageModel
import torch
# 1. 加载全精度基础模型
base_model_name = "mistral-7b-instruct-v0.3"  # 不要带bnb-4bit
model, tokenizer = FastLanguageModel.from_pretrained(
    base_model_name,
    max_seq_length=8192,
    dtype=torch.float16,  # 修正此处
    device_map="auto"
)

# 2. 加载LoRA adapter
from peft import PeftModel
model = PeftModel.from_pretrained(model, "./elysia_model")

# 3. 合并LoRA权重
model = model.merge_and_unload()

# 4. 保存为标准HF格式
model.save_pretrained("./elysia_model_fp16", safe_serialization=True)
tokenizer.save_pretrained("./elysia_model_fp16")
