# -*- coding: utf-8 -*-
# 文件: src/infer.py
# 功能: 推理与Gradio界面

from unsloth import FastLanguageModel
import gradio as gr
import torch

def infer_main():
    """
    命令行推理主入口
    """
    model, tokenizer = FastLanguageModel.from_pretrained("./elysia_model", device_map="auto")
    while True:
        user_input = input("请输入：")
        print("爱莉希雅回复：", infer(user_input, model, tokenizer))

def infer(user_input, model, tokenizer, history=None):
    """
    单轮推理函数
    """
    if history is None:
        history = []
    prompt = tokenizer.apply_chat_template(
        [{"role": "user", "content": user_input}],
        tokenize=False,
        add_generation_prompt=True
    )
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=128,  # 最大生成token数
            do_sample=True,      # 是否采样
            temperature=0.7,     # 采样温度
            top_p=0.95,          # nucleus采样阈值
            eos_token_id=tokenizer.eos_token_id,  # 终止token
            pad_token_id=tokenizer.pad_token_id   # 填充token
        )
    response = tokenizer.decode(outputs[0][inputs["input_ids"].shape[1]:], skip_special_tokens=True)
    return response.strip()

def launch_gradio():
    """
    启动Gradio网页对话界面
    """
    model, tokenizer = FastLanguageModel.from_pretrained("./elysia_model", device_map="auto")
    def user_fn(user_message, history):
        response = infer(user_message, model, tokenizer, history)
        history = history + [[user_message, response]]
        return history, history
    with gr.Blocks() as demo:
        gr.Markdown("# 爱莉希雅对话演示")
        chatbot = gr.Chatbot()
        msg = gr.Textbox(label="输入你的对话")
        clear = gr.Button("清空")
        state = gr.State([])
        msg.submit(user_fn, [msg, state], [chatbot, state])
        clear.click(lambda: ([], []), None, [chatbot, state])
    demo.launch()
