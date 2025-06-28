# -*- coding: utf-8 -*-
# 文件: main.py
# 功能: 项目主入口，支持训练、推理、网页、调参

import argparse
from src.train import train_main
from src.infer import launch_gradio, infer_main
from src.tune import tune_main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Elysia LLM 微调/推理/调参主入口")
    parser.add_argument(
        "--mode",
        choices=["train", "infer", "web", "tune"],
        default="web",
        help="运行模式，可选: train(训练), infer(命令行推理), web(Gradio网页), tune(超参数搜索)"
    )
    args = parser.parse_args()

    if args.mode == "train":
        train_main()
    elif args.mode == "infer":
        infer_main()
    elif args.mode == "web":
        launch_gradio(port=7861)  # 指定新端口
    elif args.mode == "tune":
        tune_main()
    else:
        print(f"未知模式: {args.mode}，请使用 train, infer, web 或 tune")
        parser.print_help()