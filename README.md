![Welcome](assets/welcome.gif)

# Fish spacing audit

鱼群间距的遗漏审计与共享区域复核。

```bash
pip install -r requirements.txt
python example.py
python -m unittest discover -s tests -v
```

`spacing_review.py`接收已知坐标、固定焦点和候选区域；用自己的复核服务替换`example.py`中的返回接口。输出距离上下界与已消耗面积。

**固定焦点确认不等于群体成员完整。** 几何界要求覆盖范围内参考完整、区域返回成功；面积不等同人工耗时。

示例为合成坐标，结果表来自已有数据验证。未包含原始影像、模型权重或论文。代码采用MIT许可，数据来源见[DATA_SOURCES.md](DATA_SOURCES.md)。

候选矩形须互不重叠，并覆盖所有可能返回的未知对象。结果表为受控遗漏验证；技术布局不作为独立生态重复。
