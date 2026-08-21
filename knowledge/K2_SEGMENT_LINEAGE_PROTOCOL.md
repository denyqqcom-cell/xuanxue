# K2 Segment-Aware Work Lineage Protocol

版本：2026-08-22
阶段：K2B / Deep Closure
状态：ACTIVE

## 1. 目的

`K2_SOURCE_LINEAGE.jsonl` 是 canonical source 级的一源一 work 模型；它适合单一作品载体，但无法真实表达 composite carrier。

当完整阅读已经证明一个 PDF 内含多个独立作品时，不得为了兼容旧 schema，把整个 carrier 强行绑定到其中一个 work。此协议增加一个更细的 work-family binding 层：

`CARRIER -> SEGMENT -> WORK FAMILY -> MEMBER CREDIT -> EVIDENCE`

它不删除旧 lineage，而是为旧模型表达不了的事实提供可审计的细粒度关系。

## 2. 数据文件

`knowledge/K2_SEGMENT_LINEAGE.jsonl`

每一行是一个 work-family member binding。member 可以是：

- `SOURCE`：整个 canonical source 确实只承载该 work/member；
- `SEGMENT`：只有 composite carrier 的一个已复核 segment 属于该 work/member。

禁止把已进入 `K2_SOURCE_SEGMENTS.jsonl` 的 composite source 以 `SOURCE` 身份整本绑定到某一 work family。

## 3. Work family 与 independent vote

`work_family_key` 是细粒度 family key，不冒充 legacy `work_id`。在完成 source-level lineage schema migration 前，两者保持分离。

同一 `work_family_key` 的上下册、分卷或互补 part：

- 可各自产生 unique-content evidence；
- 但 `independent_vote_key` 必须相同；
- 不能因载体数量、上下册数量或 segment 数量增加 independent evidence vote。

即：**unique coverage 可以累加，independent source vote 不可以重复计数。**

## 4. Attribution credit 必须有作用域

作者、领域、part_label 等 attribution 只能绑定到实际被证据覆盖的 member：

- `SOURCE_ONLY`：只覆盖该完整 source；
- `SEGMENT_ONLY`：只覆盖该 segment。

不得从文件名、总封面、出版社总目录或 sibling member 静默传播作者与领域。

## 5. QM-SRC-0022 / QM-SRC-0023 的当前裁决

完整视觉复核支持：

- QM-SRC-0022：整份 188 页是《甲遁真授秘錄》上册，作为一个 `SOURCE` member；
- QM-SRC-0023#SEG-001：pdf:p1-p67 是同一作品下册，作为一个 `SEGMENT` member；
- QM-SRC-0023 其余 segment 不属于这个 work family。

因此二者进入同一个 work family，但只计一个 independent vote。

## 6. 与 Evidence / Claim / Truth 的关系

Lineage 只回答“这段材料属于谁、属于哪个作品家族、能算几票”，不回答理论是否真实有效。

`LINEAGE CREDIT != METHOD CREDIT != EMPIRICAL CREDIT != TRUTH`

古籍年代、作者名望、同一作品上下册一致性，都不能自动增加 empirical credit。

## 7. 迁移纪律

在 legacy source-level lineage 尚不能表达 composite carrier 前：

- composite source 的 legacy row 可以保持 UNKNOWN；
- segment-aware binding 作为更细事实层保留；
- 不为了 schema 整齐而篡改 source facts；
- 后续迁移必须从本文件向新 schema 显式映射，不能反向用旧 row 覆盖本层事实。
