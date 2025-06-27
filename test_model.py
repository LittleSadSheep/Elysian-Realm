from unsloth import FastLanguageModel

# 加载微调好的模型和分词器
model, tokenizer = FastLanguageModel.from_pretrained("./elysia_model", device_map="auto")

# 定义对话函数
def chat_with_elysia(user_input):
    prompt = f"爱莉希雅：根据崩坏3剧情，你接下来会说：{user_input}\n"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=100)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# 测试对话
user_input = "现在情况紧急，我们需要立刻采取行动。"
response = chat_with_elysia(user_input)
print(f"爱莉希雅回复：{response}")