# -*- coding: utf-8 -*-
# 文件: src/tune.py
# 功能: 超参数自动搜索（Optuna）

import optuna
from src.train import train_main


# def tune_main():
#     """
#     Optuna自动调参入口
#     """
#     def objective(trial):
#         global use_checkpoint
#         use_checkpoint = False  # 自动调参时禁用检查点，确保每次训练都是全新开始
#         # 这里可以根据trial动态调整train_main的参数
#         # 例如：
#         # learning_rate = trial.suggest_loguniform("learning_rate", 1e-6, 5e-4)  # 学习率搜索空间
#         # per_device_train_batch_size = trial.suggest_categorical("per_device_train_batch_size", [2, 4, 8])  # batch size搜索空间
#         # lora_r = trial.suggest_categorical("lora_r", [8, 16, 32])  # LoRA秩搜索空间
#         # lora_alpha = trial.suggest_categorical("lora_alpha", [16, 32, 64])  # LoRA缩放搜索空间
#         # lora_dropout = trial.suggest_uniform("lora_dropout", 0.05, 0.3)  # LoRA dropout搜索空间
#         train_main()
#         # 假设返回验证损失
#         return 0.0
#     study = optuna.create_study(direction="minimize")
#     study.optimize(objective, n_trials=10)
def tune_main():
    # """
    # Optuna自动调参入口
    # """
    global use_checkpoint
    use_checkpoint = False  # 自动调参时禁用检查点，确保每次训练都是全新开始

    # 定义超参数搜索空间和目标函数
    def objective(trial):
        learning_rate = trial.suggest_loguniform("learning_rate", 1e-6, 5e-4)
        per_device_train_batch_size = trial.suggest_categorical(
            "per_device_train_batch_size", [2, 4]
        )  # 避免8
        lora_r = trial.suggest_categorical("lora_r", [8, 16])
        lora_alpha = trial.suggest_categorical("lora_alpha", [16, 32])
        lora_dropout = trial.suggest_uniform("lora_dropout", 0.05, 0.2)
        num_train_epochs = trial.suggest_int("num_train_epochs", 3, 7)
        return train_main(
            learning_rate=learning_rate,
            per_device_train_batch_size=per_device_train_batch_size,
            lora_r=lora_r,
            lora_alpha=lora_alpha,
            lora_dropout=lora_dropout,
            num_train_epochs=num_train_epochs,
            trial=trial,
            use_checkpoint=False,  # 关键：禁用checkpoint
        )

    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=10)
    print("最优参数:", study.best_params)
    print("最优分数:", study.best_value)
