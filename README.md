![Welcome](assets/welcome.gif)

# Fish spacing audit

鱼群间距的遗漏审计与共享区域复核。

```bash
pip install -r requirements.txt
python example.py
python -m unittest discover -s tests -v
```

`spacing_review.py`接收已知坐标、固定焦点和候选区域；用自己的复核服务替换`example.py`中的返回接口。输出距离上下界与已消耗面积。

输出固定焦点的距离上下界、确认状态及已复核面积。

示例为合成坐标，结果表来自已有数据验证。未包含原始影像、模型权重或论文。代码采用MIT许可，数据来源见[DATA_SOURCES.md](DATA_SOURCES.md)。

接口约定：候选区域互不重叠并覆盖待核查范围；每次查询返回选区内的全部记录中心。照片结果先汇总各遗漏布局，再按照片汇总；轨迹结果按记录文件汇总。
