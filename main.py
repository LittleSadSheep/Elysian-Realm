# -*- coding: utf-8 -*-
# 文件: main.py
# 功能: 项目主入口，支持训练、推理、网页、调参

import argparse
import os
import sys
import toml
from src.train import train_main
from src.infer import launch_gradio, infer_main
from src.tune import tune_main

# ========== 代理自动配置 ==========
def setup_proxy():
    config_path = os.path.join(os.path.dirname(__file__), "config.toml")
    if os.path.exists(config_path):
        config = toml.load(config_path)
        proxy_url = config.get("proxy", {}).get("url", "")
        if proxy_url:
            # 设置常见环境变量
            os.environ["HTTP_PROXY"] = proxy_url
            os.environ["HTTPS_PROXY"] = proxy_url
            os.environ["http_proxy"] = proxy_url
            os.environ["https_proxy"] = proxy_url
            # socks5 代理支持
            if proxy_url.startswith("socks5"):
                try:
                    import socket
                    import socks
                    socks.set_default_proxy(socks.SOCKS5, proxy_url.split("://")[1].split(":")[0], int(proxy_url.split(":")[-1]))
                    socket.socket = socks.socksocket
                except ImportError:
                    print("如需使用socks5代理，请先安装pysocks: pip install pysocks")
            print(f"已设置全局代理: {proxy_url}")

setup_proxy()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Elysian-Realm 微调/推理/调参主入口")
    parser.add_argument(
        "--mode",
        choices=["train", "infer", "web", "tune"],
        help="运行模式，可选: train(训练), infer(命令行推理), web(Gradio网页), tune(超参数搜索)"
    )
    args = parser.parse_args()

    # 由于choices参数已经限制了输入，只有四种模式会被接受
    # 如果没有指定--mode参数，args.mode为None，所有分支都不会进入，else会被执行
    # 如果指定了无效的mode，argparse会自动报错并退出，else分支不会被执行
    # 推荐写法如下：

    if args.mode == "train":
        train_main()
    elif args.mode == "infer":
        infer_main()
    elif args.mode == "web":
        launch_gradio(port=7861)  # 指定新端口
    elif args.mode == "tune":
        tune_main()
    else:
        # 只有在未指定--mode参数时才会进入此分支
        print("请指定有效的运行模式：train, infer, web, tune")
        parser.print_help()