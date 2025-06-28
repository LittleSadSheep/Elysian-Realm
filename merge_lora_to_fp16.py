from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

base_model_name = "mistralai/Mistral-7B-Instruct-v0.3"  # 官方原生模型
model = AutoModelForCausalLM.from_pretrained(
    base_model_name,
    torch_dtype=torch.float16,
    device_map="cpu"  # 强制全CPU
)
tokenizer = AutoTokenizer.from_pretrained(base_model_name)

# 加载LoRA adapter
model = PeftModel.from_pretrained(
    model,
    "./elysia_model",
    device_map="cpu"  # 强制全CPU
)
model = model.merge_and_unload()

# 保存为标准HF格式
model.save_pretrained("./elysia_model_fp16", safe_serialization=True)
tokenizer.save_pretrained("./elysia_model_fp16")
model.save_pretrained("./elysia_model_fp16", safe_serialization=True)
tokenizer.save_pretrained("./elysia_model_fp16")
