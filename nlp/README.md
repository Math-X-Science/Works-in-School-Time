# 在做什么？

代码所在:<br>
[Math-X-Science/school-homework](https://github.com/Math-X-Science/school-homework)<br>

我在尝试利用`deeplx`翻译英文小说，形成翻译对，然后用这些翻译对微调和从 0 训练 Transformer 模型。<br>

感谢这些仓库:<br>

- [https://github.com/CjangCjengh/YakuYaku](https://github.com/CjangCjengh/YakuYaku)
- [datawhalechina/learn-nlp-with-transformers](https://github.com/datawhalechina/learn-nlp-with-transformers/blob/main/docs/%E7%AF%87%E7%AB%A04-%E4%BD%BF%E7%94%A8Transformers%E8%A7%A3%E5%86%B3NLP%E4%BB%BB%E5%8A%A1/4.6-%E7%94%9F%E6%88%90%E4%BB%BB%E5%8A%A1-%E6%9C%BA%E5%99%A8%E7%BF%BB%E8%AF%91.ipynb)

## 关于数据集：

- 考虑到我们的数据集一半是翻译模型自动生成的。而模型碰到一些特殊词汇或者有时候算力紧张就会吐原文（英文），所以最重要的反而是把 csv 里面中文栏内含有英文的部分条目都清洗掉。因为这代表着这个段落没有被翻译完全，应该被清洗。<br>
- 关于 csv 存储的分隔问题，我最初制作数据集的时候用的是`,`，英文的，但是实际上这么做存在隐患，存在什么隐患，那就是必须保证我的中文栏目里面一个英文逗号都没有（它也确实是这样的），否则会导致读取错乱。对于这种没有处理特殊符号的数据集，BEST PRACTICE 还是用`|`。

因为数据集合并后有点大，存在 github 上面影响 clone 的时间，所以这里我打算把它抽离到网盘里。<br>

它分成这么几个部分：<br>

- origin_dataset/: 它包含原始的英文 txt 和按`\n`切分和翻译后的翻译对`csv`,用`,`分割。里面存在一些中英文混合的条目，需要清洗。<br>
- cleaned_dataset/: 它包含清洗后的翻译对`csv`，依然是用`,`分割,(我意识到地太晚了)，但因为中文里面不存在英文,所以不需要额外处理可以直接读取。<br>
- eval.csv: 我随便生成的几个翻译对，用于测试模型的效果。你可以自定义。<br>
- small.csv: 我随便挑出来的几个翻译对，用来跑通模型用的。我建议你也先验证一下模型是否能跑通最终再在大数据集上训练，因为猥琐的模型总是在最后一步才会报错。<br>
- noval.csv: 我把清洗后的数据集简单地合并和叠加到一起的结果。<br>

你可以自己对原始数据集做自己的需要的处理，比如你还可以去除掉所有短句。<br>

以及中英文混合的例子让我想起来以前训练`BERT-VITS2`的时候，在文本样例中，混合样例比较少，但是对于说话的场景，那中英文混合的案例就太多了：<br>

- 比如说我们这个 tensor 啊。
- pytorch 真的是太好用了。
- coding 能力要怎么样才能快速提升或者稳步提升？

这样子的样例太多了。<br>

所以我觉得中英文混在一起做`tokenize`应该是没有问题的，甚至可能会在上面的问题上表现的不错。后面 BERT-VITS2 也确实出了一个支持中英文混合的模型，但我当时已经没有再跟进了，没看细节。<br>

但那种混合的情况数据集太难找了。把各种音素的混合训练到，哪怕只是单语言就够喝一壶了，混合的话，数据集的均衡性非常难保证。<br>

数据集网盘地址:<br>

```txt
english-novel-complete-works
链接: https://pan.baidu.com/s/1eh4D0at0ONT7Ct89V0Mw8g?pwd=1tt3 提取码: 1tt3
```

## 分词：

之前训练大模型的时候比较方便，tokenizer 和 embedding 都是由模型开发的人提供的，只需要做好指令微调的数据集喂进去，然后等就行。<br>

但如果自己训练自定义的模型，那么对于 embedding 和 tokenizing 都是自己要考虑的。<br>

因为在大样本集上面的分词和 embedding 通常要很久，所以先在 demo 上面演示.<br>

这里的一个点是：是否要把中英文的 indices 建立在一个词典下？<br>

我选择把 indices 分别建立在两个词典下，因为我的用例中完全不存在："我喜欢 Python" -> "I like Python" 这样的情况。我翻译的是小说。我更希望在 Embedding 的时候两个字典存在于不同的空间，然后让模型自己学着映射，而不是一开始就存在一些关联。<br>

当然如果字典本身比较小，偏日常用语，且里面也有不少：“这个 to_tensor...”这样的混合用例，那么建立在一个空间应该是不错的选择，至少经常出现在一起的组合在 embedding 之初就有联系。<br>

这里是一些 token 和 indices:<br>

```shell
tokens     ([这是, 果酱, ！], [This, is, jam, !])
indices    ([49, 310, 7], [7, 308, 9, 10])
Name: 20, dtype: object
```

```shell
tokens     ([两个, 女孩, 拉住, 了, 对方, ，, 一个, 扮演, 绅士, ，, 另一个, ...
indices    ([98, 81, 103, 14, 101, 3, 31, 104, 105, 3, 83...
Name: 3, dtype: object
```

![image-20250106213904048](https://fastly.jsdelivr.net/gh/MrXnneHang/blog_img/BlogHosting/img/25/01/202501062322450.png)

demo 上的中英文非重复分词长度。<br>

如果直接用 BERT 做 Embedding 的话，通常不需要考虑这么多，直接少走弯路。后面也会在第一个模型训练完后改用 BERT 进行一个对比。<br>

## Embedding

这里因为之后要和预训练的 BERT 做对比，所以 Embedding 相当水，只是简单投射了一下。

```python
class Embeddings(nn.Module):
    def __init__(self, d_model, vocab):
        super(Embeddings, self).__init__()
        self.lut = nn.Embedding(vocab, d_model)
        self.d_model = d_model

    def forward(self, x):
        return self.lut(x) * math.sqrt(self.d_model)
```

在初始化的时候，我们的 embedding 是随机初始化的，不过我们把 indices 分开了。相当于到时候会产生两个 Embedding 空间，一个是中文的一个是英文的。

它会随着我们的训练而更新，像是模型的一部分，优点是可以更贴合任务进行参数调整。

缺点就是，可调参数太多对训练的难易度是很大挑战。这些缺点可以用微调预训练模型来进行一个弥补。

![image-20250106224552556](https://fastly.jsdelivr.net/gh/MrXnneHang/blog_img/BlogHosting/img/25/01/202501062322412.png)

似乎数据集太小，二十秒左右就 loss<0.4 了，按理来说 NLP 的任务 Seq2Seq Loss 不应该将太低，这说明模型把所有数据都记住了，而且还没怎么更新到 embedding。于是下一步是，扩大数据集。

### 一个彩蛋：

前面提到我的 demo 相当小，然后在可视化和测试的时候就出现了很有意思的点。因为我的 embedding 是自定义的，而里面没有 test 这个词。于是乎它就映射到了果酱:（有点幽默）

![image-20250106230908256](https://fastly.jsdelivr.net/gh/MrXnneHang/blog_img/BlogHosting/img/25/01/202501062322954.png)

它来源于训练集：<br>

```shell
tokens     ([这是, 果酱, ！], [This, is, jam, !])
indices    ([49, 310, 7], [7, 308, 9, 10])
Name: 20, dtype: object
```

this is a jam, 这是一个测试。<br>

到目前为止模型在预期的范围内工作。下一步就是扩大数据集然后躺平等训练了。<br>

## 扩大我们的训练集并且给我们的实验画上句号。
