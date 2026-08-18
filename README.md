# Xuanxue

离线优先的六术排盘与知识工程项目。当前正式治理域为：紫微斗数、八字、奇门遁甲、六爻、大六壬、风水；黄历/历法作为公共基础服务。

## 当前研发主线

项目同时维护两条线：

1. 稳定 App 基线；
2. Knowledge Engine v1。

Knowledge Engine 当前位于 K2B Evidence Extraction。K1 Source Registry 与 K2A Source Lineage 已完成项目端闭环，但 Claim Extraction 仍保持锁定。

### K2B 执行权

K2B 的仓库代码、Schema、validator、正式 Reading Ledger、Atomic Evidence、Git commit/push 与阶段验收由项目主 Agent 负责。

本地 AI 仅作为执行助手：

- fetch/pull；
- 运行项目端已有脚本/测试；
- 在本机寻找 canonical source bytes；
- 机械生成或回传 page packet；
- 报告环境失败。

本地 AI不得修改 tracked 文件、归纳正式 Evidence、创建 Claims、修改 App/算法、commit 或 push。

Source identity 以 K1 canonical `file_sha256` 为唯一字节身份依据。旧 private intake 的 `local_path` 只是可选定位线索；如果 private registry 不在当前机器，可以在明确指定的本地 corpus roots 中按 SHA256 找到完全相同的源文件。文件名或标题相似不能替代 hash identity。

## 隐私与版权边界

App 不依赖账号、广告、支付、推送或业务服务器，稳定基线不申请 INTERNET 权限。

原书 PDF、扫描页、OCR 全文、local page packets 与现代书长段文字不进入 `knowledge/`，也不打包进 APK。Git 只保存独立改写后的结构化事实、页码定位、来源哈希、谱系、规则契约、测试与可复现 fixture。

## 六术知识成熟度

当前六域统一从 `L1_INDEXED` 起跑。历史上已经形成的奇门 claims / fixtures 保留为 legacy pending re-audit，不自动享受更高成熟度。

成熟度顺序：

`L0_SOURCE_ONLY → L1_INDEXED → L2_CLAIM_EXTRACTED → L3_CROSS_VERIFIED → L4_CONFLICT_MAPPED → L5_FIXTURE_VERIFIED → L6_ENGINE_VERIFIED → L7_INTERPRETATION_READY → L8_FEEDBACK_VALIDATED`

具体阶段与 Gate 以 `knowledge/STATUS.md`、`knowledge/PROJECT_STATE.json` 和对应 validator 为准。

## Knowledge Engine 原则

- Source / Evidence / Claim / School / Conflict / Fixture / Case 分层；
- 同一作品的不同扫描版不能重复计票；
- WORK_PART 有独特 coverage 必须读，但不能视作新的独立来源；
- NOTE / CODE / AUX 不作为传统术理文本证据；
- Evidence 只回答“这一本书这一页明确支持什么”；
- Claim 才负责后续归一化；
- Conflict 不靠多数票消除；
- 所有算法进入 Engine 前必须有来源、可复现 fixture 和回归测试；
- 六术共同使用知识工程协议，但保留各自 ontology、流派树与解释边界。

## 构建

核心回归：

```bash
./gradlew --no-daemon :ziwei-core:test
```

Knowledge Engine Gate 由 `.github/workflows/knowledge-engine-ci.yml` 执行，其中包含 Linux 主 Gate 和 Windows K2 helper portability test。

## 免责声明

本项目中的命理、术数和风水内容属于传统文化/研究与软件实现范畴，不应代替医疗、法律、财务或其他专业意见。
