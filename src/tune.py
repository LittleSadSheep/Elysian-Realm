# -*- coding: utf-8 -*-
# 文件: src/tune.py
# 功能: 超参数自动搜索（Optuna）

import os
import sys
import optuna
from src.train import train_main

# ========== 代理自动配置 ========= =
import toml
def setup_proxy():
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.toml")
    if os.path.exists(config_path):
        config = toml.load(config_path)
        proxy_url = config.get("proxy", {}).get("url", "")
        if proxy_url:
            os.environ["HTTP_PROXY"] = proxy_url
            os.environ["HTTPS_PROXY"] = proxy_url
            os.environ["http_proxy"] = proxy_url
            os.environ["https_proxy"] = proxy_url
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

def tune_main():
    """
    Optuna自动调参入口
    """
    def objective(trial):
        # 这里可以根据trial动态调整train_main的参数
        # 例如：
        # learning_rate = trial.suggest_loguniform("learning_rate", 1e-6, 5e-4)  # 学习率搜索空间
        # per_device_train_batch_size = trial.suggest_categorical("per_device_train_batch_size", [2, 4, 8])  # batch size搜索空间
        # lora_r = trial.suggest_categorical("lora_r", [8, 16, 32])  # LoRA秩搜索空间
        # lora_alpha = trial.suggest_categorical("lora_alpha", [16, 32, 64])  # LoRA缩放搜索空间
        # lora_dropout = trial.suggest_uniform("lora_dropout", 0.05, 0.3)  # LoRA dropout搜索空间
        train_main()
        # 假设返回验证损失
        return 0.0
    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=10)
