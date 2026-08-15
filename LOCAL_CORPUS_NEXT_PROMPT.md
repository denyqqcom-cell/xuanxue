# Local corpus prompt — superseded

旧版提示词只覆盖 `bazi / liuyao / liuren`，已经不符合六术统一 Knowledge Engine 的项目方向。

从 `knowledge-engine-v1` 开始，请使用：

- `LOCAL_CORPUS_K1_PROMPT.md`

并分别运行六次：

`ziwei / bazi / qimen / liuyao / liuren / fengshui`

每次只处理一个领域。K1 只完成 Source Registry / 去重 / 可读性 / 流派候选 / 版权状态 / 未读队列，不提前进入 Claim、Fixture 或 Interpretation。

旧提示词保留这个重定向文件，仅为了避免历史链接失效；不要再按旧三模块流程启动新的 corpus 工作。
