正在核对结果并收尾。**2026-W41 购物垂类的点击率是 36.97%**(39,857 次点击 / 107,810 次搜索,共 900 个查询)。

```
## Answer
Headline: 36.97 %(95% 区间:未计算,见下)
2026-W41 购物垂类(electronics、apparel、home)的点击率为 36.97%;若不先对 query_category 去重,会错报成 40.90%。
- Observed: 36.97 %(95% 区间:未计算;这是全量汇总值,不是抽样估计)
- Adjusted: not computed(问的是单周的水平值,没有需要调整的对比)
- Causal effect: not identified(这是描述性指标,不涉及干预;要识别因果需要有对照的实验)

## What it means for 商品运营(Merchandising)引用该数字
应引用 36.97%,不要引用 40.90%。两者相差 3.9 个百分点,足以改变任何以 40% 为界的判断。只有当决策阈值落在 36.97% 附近且差距小于抽样误差时,才需要补区间。

## Why we believe it
- Alternatives considered:
  - 直接 join query_category:已排除。该表有 250 条重复行(2250 行对应 2000 个查询,即 electronics、apparel、home 的 2026-10-09 重复加载)。直接 join 会让 250 个购物查询被重复计算,得到 1150 行、40.90% [measured]
  - 同一查询在两次加载中类别不同:已排除。类别不一致的查询数为 0,所以按 (query_id, category) 去重是安全的 [measured]
  - 有查询没有类别:已排除。query_week 中无类别的查询数为 0 [measured]
  - 垂类映射缺失:已排除。5 个类别全部映射,购物 = electronics + apparel + home [measured]
- Checks run:
  - fanout(直接 join):fail。右表多出 250 行,join 后膨胀 250 行
  - fanout(去重后):pass。900 行对 900 行,无膨胀
  - completeness:could not run。库里只有 W41 一周,没有前几周可比。W41 是 10-05 至 10-11,今天是 10-14,按日历已结束,但无法验证数据是否加载完整
  - srm、mix_shift:skipped。这不是实验,也没有前后对比
  - 数据质量:空值和 clicks>searches 均为 0 行 [measured]

## Caveats, and what would change the answer
- 未验证 W41 是否完整加载。W41 的 2000 行查询与类别表的 2000 个查询一一对应,但没有历史周可对照。
- 点击率按总点击除以总搜索(加权)计算。若 Merchandising 要的是各查询点击率的简单平均,数字会不同。
- 三个购物类别的点击率几乎一样(各约 37%),所以结论对类别构成不敏感。

## Provenance
- Metric: 点击率 = sum(clicks) / sum(searches),垂类为 shopping,来自 stated here [guess];目录里没有 metrics.json
- Data: query_week、query_category(去重后)、category_vertical,截至 2026-W41(库里唯一一周)
- Reconciled: not done(没有可对照的看板或外部来源)
- Queries and checks: 查询是本次会话内联运行的 SQLite 查询,未保存成文件;检查结果记录在工作目录的 .ds-checks.log(fanout#1、fanout#2、completeness#1)
```