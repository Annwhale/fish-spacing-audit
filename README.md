![Welcome](assets/welcome.gif)

# Fish spacing audit

[中文](#中文) · [English](#english)

## 中文

鱼群间距的遗漏审计与共享区域复核。

`spacing_review.py`接收已知坐标、固定焦点和候选区域，输出距离上下界、确认状态及已复核面积。用自己的复核服务替换`example.py`中的返回接口即可使用。

接口约定：候选区域互不重叠并覆盖待核查范围；每次查询返回选区内的全部记录中心。照片结果先汇总各遗漏布局，再按照片汇总；轨迹结果按记录文件汇总。

仓库提供合成坐标示例及验证结果汇总表。代码采用 MIT 许可，数据来源见[DATA_SOURCES.md](DATA_SOURCES.md)。

## English

Omission audits and shared regional review for fish-spacing measurements.

`spacing_review.py` takes known coordinates, fixed focal individuals and candidate regions, and returns distance bounds, confirmation status and reviewed area. To use it with your own workflow, replace the return interface in `example.py` with your review service.

Interface contract: candidate regions are non-overlapping and cover the area to be reviewed; each query returns all recorded object centres within the selected region. Photo results are aggregated across omission layouts within each photograph, then across photographs; trajectory results are aggregated by recording.

The repository provides a synthetic-coordinate example and summary tables from the validation analyses. Code is released under the MIT licence; data sources are listed in [DATA_SOURCES.md](DATA_SOURCES.md).

## 快速开始 / Quick start

```bash
pip install -r requirements.txt
python example.py
python -m unittest discover -s tests -v
```
