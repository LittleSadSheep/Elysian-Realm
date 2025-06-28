# 往事乐土 Elysian-Realm <img align="right" src="./Elysia.jpg" width="320"/>
> **回应我吧，爱莉希雅！！**<br>
> **赐予爱莉希雅——第二次生命！！**<br>

- 本项目使用QLoRA方法微调LLM，使爱莉希雅获得第二次生命

## 训练模型
### 环境配置
- Python 3.10
- CUDA GPU

## 使用方法

### 1. 准备运行环境
   - 安装python ~~去官网下，这不用我教吧~~
   - 安装依赖
   ```BASH
      pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu126
      pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

### 2. 准备数据集
   - 你需要在根目录下准备好数据集，格式**严格遵循**`ShareGPT Fomat`，并将其保存在项目根目录下，保存为`json`格式<br>
      以下是例子：<br>
   ```JSON
      [
         {
            "conversations": [
               {
                  "from": "human",
                  "value": "芽衣：这些敌人也都是你的「记忆」吧？看来它们不太欢迎我呢。但我没想到，连你都会受到攻击。"
               },
               {
                  "from": "gpt",
                  "value": "爱莉希雅：不用那么惊讶，这里是有些与众不同，但毕竟也是「往世乐土」的一部分，和你见过的其他区域原理相同，没什么差别。 哦对，还没向你正式介绍呢。刚才说到一半就被这群小家伙打断了…… 欢迎来到由「至深之处」保存的，往世乐土最深的秘密—— 由「爱莉希雅」的记忆组成的，完全还原「爱莉希雅」一生所爱的，「爱莉希雅」的心象世界。 如你所见，它就像一切美丽事物的凝聚，和平而永恒的梦幻仙境，立于所有理想尽头的无瑕乐园。 不知道「永世乐土」这个名字……能否让你充满好奇呢？"
               }
               // ......  
               // 可有多组对话
            ]
         }
         // ......  
         // 可有多个conversations
      ]
   ```
### 3. 调整训练参数并启动微调训练 
   - 运行`finetune_elysia.py`启动模型微调
   ```bash
   python ./finetune_elysia.py
   ```

#### 训练参数调整说明

- **对模型质量的影响：**
  - `num_train_epochs`：训练轮数，越大模型越能拟合数据，但过大易过拟合。小数据集建议3-5，大数据集可适当增加。
  - `learning_rate`：学习率，过大易震荡，过小收敛慢。一般`2e-5`~`5e-5`，小数据集建议更小。
  - `per_device_train_batch_size`：每卡batch size，越大训练越快但显存占用高。小显存建议1-2，大显存可4-8。
  - `gradient_accumulation_steps`：梯度累积步数，配合batch size调节显存压力。
  - `lora_alpha`、`r`：LoRA参数，越大表达能力越强但显存占用高。
  - `early_stopping_patience`：早停耐心，防止过拟合。

- **对机器性能的影响：**
  - `per_device_train_batch_size`、`gradient_accumulation_steps`：直接影响显存占用。
  - `dataloader_num_workers`：数据加载线程数，CPU多可适当增大。
  - `gradient_checkpointing`：开启可节省显存但训练变慢。
  - `fp16`/`bf16`：混合精度加速，建议开启。

#### 参数调整方法

- 修改 `finetune_elysia.py` 中 `TrainingArguments` 相关参数即可。
- 例：  
   ```python
   training_args = TrainingArguments(
      num_train_epochs=5,
      learning_rate=2e-5,
      per_device_train_batch_size=2,
      gradient_accumulation_steps=2,
      # ...其他参数...
   )
  ```


### 4. 使用TensorBoard观察训练并调整参数

- 启动训练时会自动记录日志到 `./logs` 目录。
- 训练过程中可用如下命令实时查看曲线：
  ```bash
  tensorboard --logdir=./logs --host=0.0.0.0
  ```
- 浏览器访问 http://localhost:6006 查看loss、perplexity等指标曲线。
- 根据曲线调整参数：
  - loss下降缓慢：可适当增大学习率或训练轮数。
  - loss震荡或上升：可减小学习率或增大early stopping耐心。
  - 验证集loss早早不降：可减少epoch或增大early stopping耐心。

### 5. 简单测试模型
   - 你可使用`test_model.py`对模型进行简单测试
   ```bash
   python ./test_model.py
   ```
   - 在显示`请输入：`时可以进行输入
### 6. 导出GGUF格式（llama.cpp推理）合并LoRA权重并导出FP16模型

- 训练完成后，运行`merge_lora_to_fp16.py`将LoRA权重合并到全精度基础模型，导出标准HuggingFace格式：
  ```python
   python ./merge_lora_to_fp16.py
  ```
- 使用llama.cpp的转换脚本，将合并后的模型目录导出为GGUF格式：
  ```bash
  python llama.cpp/convert_hf_to_gguf.py ./elysia_model_fp16 --outfile ./output.gguf
  ```
- 注意：只能用合并后的全精度模型目录（如`elysia_model_fp16`），不能用adapter目录直接转换。

---

## 注意事项
> 本应用生成内容来自人工智能模型，由 AI 生成，请仔细甄别，请勿用于违反法律的用途，AI 生成内容不代表本项目团队的观点和立场。

## 贡献者

<a href="https://github.com/LittleSadSheep/Elysian-Realm/graphs/contributors">
  <img alt="contributors" src="https://contrib.rocks/image?repo=LittleSadSheep/Elysian-Realm" />
</a>

## Star历史

[![Star History Chart](https://api.star-history.com/svg?repos=LittleSadSheep/Elysian-Realm&type=Date)](https://star-history.com/#LittleSadSheep/Elysian-Realm&Date)

欢迎PR和Star！


---

如有问题欢迎提issue或讨论！
