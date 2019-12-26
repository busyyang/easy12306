
<center><font size=5>easy12306学习记录</font></center>

### 运行顺序
1. 运行`pretreatment.py`得到`data.npz`数据集，里面包含所有的`labels`的图片数据，以及所有待选择图片的`whash`值。
2. 保存好了`data.npz`后，运行`baidu.py`,从百度OCR的API去识别这些`labels`上面的文字。并保存到`texts.log`中。
3. 运行`get_top80_category.py`，通过频次统计，发现其实12306的验证码图片就80类，获取这80类识别正确的labels图片与识别结果，作为`texts.npz`数据集，识别的80类（高频）放在了`text_top_80.txt`中。由于我爬取的图片只有8000多张，正确识别的只有4800张左右，识别的80类还是有点问题，具体的80类可以参考[zhaipro/easy12306的repo](https://github.com/zhaipro/easy12306/blob/master/texts.txt)，用这个文件替换`text_top_80.txt`。
4. 用生成的`texts.npz`作为数据集，跑`mlearn.py`文件，运行其中的main函数，得到`models.v1.0.h5`模型。

