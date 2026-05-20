# AI Engineering ROI Calculator

Companion to *Software Engineering with AI* by Ryan Byrd · Ch 54 §54.5

This is the agent-readable source of the ROI model. The rendered spreadsheet (formerly `executive-strategic-kit/roi-calculator.xlsx`) can be regenerated from this markdown — see the "Building the spreadsheet" section at the end. The markdown source is the source of truth so the model is legible to both humans and agents (Ch 6 §6.0).

## How to use this model

Fill in the **Conservative / Base / Aggressive** columns with your numbers. The formulas in the Outputs section derive everything from those inputs. Three scenarios let you stress-test what you commit to in writing.

## Inputs — Engineering org parameters

| Input | Conservative | Base | Aggressive | Notes |
|---|---|---|---|---|
| Total engineers (full org) | 60 | 60 | 60 | Headcount as of plan date. Use total org, not just AI users. |
| Loaded cost per engineer ($/year) | 220,000 | 240,000 | 260,000 | Salary + benefits + overhead. Mid-size US 2026 typically $200K–$280K. |
| Coding utilization factor | 0.55 | 0.60 | 0.65 | Fraction of eng time on coding (vs meetings, support, on-call). Typical: 0.55–0.70. |
| AI tool adoption rate | 0.60 | 0.80 | 0.95 | Fraction of eligible engineers actively using AI tooling >2x/week. |
| Productivity gain on AI-assisted work | 0.08 | 0.12 | 0.18 | Year 1: 5–15% prepared teams. Above 15% requires very mature harness. |

## Inputs — Annual cost ($/year)

| Cost line | Conservative | Base | Aggressive | Notes |
|---|---|---|---|---|
| Tooling spend (per-seat licenses) | 90,000 | 130,000 | 180,000 | Cursor / Copilot / Claude Code seats × N. Scales with adoption. |
| Token / API spend | 60,000 | 95,000 | 145,000 | Per-dev median × weeks × adopters. Higher with more agentic use. |
| Harness investment (engineer time) | 80,000 | 120,000 | 200,000 | FTE equivalent. 0.5 FTE for 60-eng org typical. |
| Governance overhead (CISO, GC, legal) | 20,000 | 30,000 | 50,000 | Vendor reviews, customer Q&A, audits. |

## Outputs — ROI

```
Annual productivity gain ($) = engineers × loaded_cost × utilization × adoption × productivity_gain
Total annual cost ($)        = tooling + tokens + harness + governance
Net ROI ($)                  = productivity_gain - total_cost
ROI multiple                 = productivity_gain / total_cost
Per-engineer net ROI ($)     = net_ROI / engineers
```

Base-case worked numbers (60 engineers, $240K loaded cost, 0.60 utilization, 0.80 adoption, 12% productivity gain):

| Metric | Value |
|---|---|
| Annual productivity gain | $1,036,800 |
| Total annual cost | $375,000 |
| **Net ROI** | **$661,800** |
| ROI multiple | 2.77x |
| Per-engineer net ROI | $11,030 |

## Sensitivity — Net ROI vs productivity gain (Base case, all else equal)

| Productivity gain | 5% | 8% | 10% | 12% | 15% | 18% | 20% | 25% |
|---|---|---|---|---|---|---|---|---|
| Productivity gain ($) | $432K | $691K | $864K | $1,037K | $1,296K | $1,555K | $1,728K | $2,160K |
| Net ROI ($) | $57K | $316K | $489K | $662K | $921K | $1,180K | $1,353K | $1,785K |
| ROI multiple | 1.15x | 1.84x | 2.30x | 2.77x | 3.46x | 4.15x | 4.61x | 5.76x |

### How to read this

- Each column is a scenario where productivity gain is the only thing that changes; all other Base assumptions hold.
- If your honest measured productivity gain is below 8%, you may not be net-positive. Audit cost discipline first.
- Above 15%, claims start to need exceptional evidence. Most mid-size teams should plan for 8–15% in year one.
- The relationship is roughly linear — each 1% of productivity gain adds ~$90K to net ROI at 60 engineers.

## 12-month token spend forecast (Base case)

Assumes a linear ramp from 50% to 100% of full token spend over the first 6 months.

| Month | M1 | M2 | M3 | M4 | M5 | M6 | M7–M12 |
|---|---|---|---|---|---|---|---|
| Monthly token spend ($) | $3,958 | $4,592 | $5,304 | $5,938 | $6,571 | $7,283 | $7,917 |

Cumulative spend reaches roughly $95K by month 12. Add a **15% buffer** on top for batch workloads (test generation runs, mass refactors) not captured in per-developer median. If batch workloads are large in your org, model them as separate line items.

## Notes for the CFO conversation

- Productivity gain is the most sensitive input. Each 1% is roughly $90K at 60 engineers.
- Adoption rate is the second most sensitive. Realistic mid-size adoption is 60–80% in year one.
- Token spend can swing 2–3x based on routing discipline (Sonnet vs Opus, retry control). See Ch 26.
- Harness investment as engineer time is real cost; do not exclude it just because it's not a separate line item.
- Year 2 economics improve materially as harness compounds. This model is year 1.
- Substitution posture (cuts + AI) requires modifying the productivity gain assumption downward — see Ch 54 §54.7.

## Building the spreadsheet (if you want the xlsx render)

The companion repo includes `scripts/render-roi-calculator.py` (forthcoming) which reads this markdown and emits a `.xlsx` with the formulas wired up. For now, copy the Inputs tables into Excel/Numbers and apply the Outputs formulas. The agent-readable markdown above is the canonical source — if you change the model, change this file and re-render, not the other way around.
