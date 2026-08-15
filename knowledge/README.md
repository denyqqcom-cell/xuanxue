# Xuanxue Knowledge Engine v1

`knowledge/` 是紫微、八字、奇门、六爻、大六壬、风水六术的统一知识工程层。它不保存现代书籍全文，也不把“书里写了”直接等同于“程序可以采用”。

六术统一经过：`Source -> Evidence -> Claim -> Conflict/School -> Fixture -> Engine -> Selection -> Interpretation -> Feedback`。

## 六术与公共层

- `ziwei` 紫微斗数
- `bazi` 八字
- `qimen` 奇门遁甲
- `liuyao` 六爻
- `liuren` 大六壬
- `fengshui` 风水
- `common` 只放跨术共享的历法/干支/节气/五行等基础事实；共享基础不等于共享解释。

黄历是公共历法/民俗工具，不作为第七个术数域参与六术成熟度竞赛。

## 三层硬边界

1. `STRUCTURE`：可确定计算的历法、排盘、装卦、起课、坐向等结构。
2. `SELECTION`：用神、类神、主客、宫位/对象选择，必须绑定具体事体和流派。
3. `INTERPRETATION`：综合关系、情境推演、反证、应期和置信边界。

Structure 已验证，不代表 Selection/Interpretation 自动开放。

## 成熟度

采用 L0-L8：SOURCE_ONLY、INDEXED、CLAIM_EXTRACTED、CROSS_VERIFIED、CONFLICT_MAPPED、FIXTURE_VERIFIED、ENGINE_VERIFIED、INTERPRETATION_READY、FEEDBACK_VALIDATED。

整个领域的 level 采用保守口径：只能表示该领域整体已达到的最低共同层，不以单条强规则抬高全域成熟度。

## 版权

公开 Git 只保存来源元数据、独立重写的事实/程序规则、冲突、fixture 与派生统计。现代 PDF、扫描页、全文 OCR、现代长译注、独创图表、未知许可字体/图片默认不得进入本目录或 APK。

古籍底本与现代扫描/整理/标点/翻译/排版是不同版权对象，必须分开记录。

## K0 状态

K0 只建设统一 schema、六域骨架、验证器和状态生成机制。`qimen` 仅引用现有 handoff 作为 legacy import，不因此提高其他五域成熟度。K1 才进行六术全量本地书籍盘点。
