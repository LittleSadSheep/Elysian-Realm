
# 往事乐土 Elysian-Realm <img align="right" src="./Elysia.jpg" width="320"/>
**回应我吧，爱莉希雅！！**</br>
**赐予爱莉希雅——第二次生命！！**
本项目使用QLoRA方法微调LLM，使爱莉希雅获得第二次生命

## 训练模型
### 环境配置
- Python 3.10
- PyTorch 2.0
- Transformers 4.26
- Datasets 2.10
- Tokenizers 0.13
- Scikit-learn 1.2
- Matplotlib 3.5
- TensorBoard 2.12
- Jupyter Notebook
### 数据预处理
1. 下载并预处理原始数据集（如Elysian-Realm）
2. 划分训练集和验证集
3. 构建自定义数据集类
### 模型训练
1. 加载预训练模型
2. 配置训练参数
   - 学习率、批次大小、训练步数
   - 优化器、损失函数、学习率调度器
3. 定义训练和评估函数
4. 启动训练循环
   - 加载检查点（可选）
