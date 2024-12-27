# 在做什么?

我在微调 Qwen-7B-Chat 模型,让它能够像一个医生一样回答问题。<br>

之所以接这个任务是想着为之后微调赛博女朋友做准备,同时测试一下我机器的性能.去年买来原本就是打算玩玩大模型,但是玩了一阵子 tts 就没玩下去了,感觉错失很多.<br>

我总是慢一步.<br>

## 关于数据集

数据集是一个中医和患者的对话数据集,来源于[zhangsheng93/cMedQA2](https://github.com/zhangsheng93/cMedQA2).<br>

我简单地经过清洗,然后把它做成了指令微调的格式.<br>

简单预览:<br>

```json
{
    "instruction": "头痛头昏十几年前。吹风和晒太阳。吵闹都会头疼没有检查出来结果应该怎样治疗",
    "input": "",
    "output": ":考虑是神经性头疼，是一种功能性的疾病，是由于紧张压力或是精神因素引起的神经功能失调造成的头痛，也有一定的遗传因素，一般可考虑吃些中草药川芎茶调散来治疗。同时结合针灸按摩，效果会更好的。"
},
{
    "instruction": "眼睛疲劳，老睁不开干涩",
    "input": "",
    "output": "一般是由于结膜炎症活干炎症引起的，可以到医院检查一下。"
},
{
    "instruction": "女人的左胸下是什么地？那里痛是怎么回事",
    "input": "",
    "output": "心脏在那个位置，心脏绞痛在那，也可能是胃痛导致的，胃痛位置比心脏偏下一点。"
}
```

你也可以省事情直接用我整理好后的.<br>

```txt
链接: https://pan.baidu.com/s/1iDjjGgUz9T6yYWbkVnfLGQ?pwd=eh4t 提取码: eh4t
```

## 过程和 bug:

- [课设延伸: 记录本地指令微调 Qwen-7B-Chat 的过程](https://xnnehang.top/blog/182)
- [LLaMA-Factory 模型导出和断点续训](https://xnnehang.top/blog/183)
- [gradio 调用 fastapi 超时 | localhost is not accessible | share=True | 跨域请求](https://xnnehang.top/blog/184)

我一般习惯边做边写,不太喜欢总结,所以这里就直接放 link 了.<br>
