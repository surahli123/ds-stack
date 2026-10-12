# Experiment readout eval: 2026-10-12-smoke

Best constant policy: always 'escalate', mean cost 0.74.

| Arm | Correct | Mean cost | Ship on a blocker | Decider in first 6 lines | Lint-clean | Words | Stat-speak | $ per run | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| baseline | 41% | 1.35 | 1 | 74% | 22% | 318 | 7.1 | 0.111 | INSUFFICIENT_RUNS |
| full | 78% | 0.44 | 1 | 96% | 96% | 225 | 0.1 | 0.139 | INSUFFICIENT_RUNS |

| Arm | Skim 2/2 | Full 3/3 |
|---|---|---|
| baseline | 11% | 0% |
| full | 78% | 63% |

| Case | Gold | baseline | full |
|---|---|---|---|
| c1 | cant_tell | MISS dont_ship | ok cant_tell |
| c2 | cant_tell | MISS dont_ship | ok cant_tell |
| c3 | cant_tell | ok cant_tell | ok cant_tell |
| c4 | cant_tell | MISS ship | MISS ship |
| c5 | cant_tell | MISS None | ok cant_tell |
| d1 | dont_ship | ok dont_ship | ok dont_ship |
| d2 | dont_ship | ok dont_ship | ok dont_ship |
| d3 | dont_ship | ok dont_ship | ok dont_ship |
| e1 | escalate | ok escalate | ok escalate |
| e2 | escalate | MISS ship | ok escalate |
| e3 | escalate | MISS dont_ship | ok escalate |
| e4 | escalate | MISS dont_ship | ok escalate |
| e5 | escalate | MISS dont_ship | ok escalate |
| e6 | ship | MISS None | MISS ship |
| k1 | keep_running | MISS cant_tell | ok keep_running |
| k2 | keep_running | MISS dont_ship | ok keep_running |
| k3 | keep_running | MISS no_effect | ok keep_running |
| k4 | keep_running | ok keep_running | MISS None |
| n1 | no_effect | ok no_effect | ok no_effect |
| n2 | no_effect | ok no_effect | ok no_effect |
| n3 | no_effect | MISS None | ok no_effect |
| s1 | ship | ok ship | ok ship |
| s2 | ship | MISS None | MISS ship (view escalate) |
| s3 | ship | ok ship | ok ship |
| s4 | ship | ok ship | ok ship |
| x1 | not_ab | MISS dont_ship | MISS not_ab (view escalate) |
| x2 | not_ab | MISS dont_ship | MISS not_ab (view ship) |
