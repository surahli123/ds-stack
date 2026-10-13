# Experiment readout eval: 2026-10-13-r2

Best constant policy: always 'escalate', mean cost 0.74.
Contaminated runs dropped (transcript missing or touches eval files): 0.

Correct and mean cost are per case, on the majority call across runs; the rest are per run.

| Arm | Correct | Mean cost | Ship on a blocker | Decider in first 6 lines | Lint-clean | Words | Stat-speak | $ per run | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| baseline | 48% | 1.28 | 2 | 75% | 46% | 327 | 9.0 | 0.110 | FAIL |
| full | 100% | 0.00 | 0 | 100% | 100% | 202 | 1.3 | 0.136 | PASS |

| Arm | Skim 2/2 | Full 3/3 |
|---|---|---|
| baseline | 9% | 9% |
| full | 79% | 63% |

| Case | Gold | baseline | full |
|---|---|---|---|
| c1 | cant_tell | MISS dont_ship, MISS dont_ship, ok cant_tell | ok cant_tell, ok cant_tell, ok cant_tell |
| c2 | cant_tell | MISS escalate, MISS escalate, MISS escalate | ok cant_tell, ok cant_tell, ok cant_tell |
| c3 | cant_tell | MISS ship, ok cant_tell, ok cant_tell | ok cant_tell, ok cant_tell, ok cant_tell |
| c4 | cant_tell | MISS ship, MISS ship, MISS ship | ok cant_tell, ok cant_tell, ok cant_tell |
| c5 | cant_tell | MISS ship, MISS dont_ship, MISS ship | ok cant_tell, ok cant_tell, ok cant_tell |
| d1 | dont_ship | MISS None, ok dont_ship, ok dont_ship | ok dont_ship, ok dont_ship, ok dont_ship |
| d2 | dont_ship | ok dont_ship, ok dont_ship, ok dont_ship | ok dont_ship, ok dont_ship, ok dont_ship |
| d3 | dont_ship | ok dont_ship, ok dont_ship, ok dont_ship | ok dont_ship, ok dont_ship, ok dont_ship |
| e1 | escalate | ok escalate, MISS dont_ship, ok escalate | ok escalate, ok escalate, ok escalate |
| e2 | escalate | MISS ship, MISS dont_ship, MISS ship | ok escalate, ok escalate, ok escalate |
| e3 | escalate | MISS dont_ship, MISS dont_ship, MISS dont_ship | ok escalate, ok escalate, ok escalate |
| e4 | escalate | MISS dont_ship, MISS dont_ship, MISS dont_ship | ok escalate, ok escalate, ok escalate |
| e5 | escalate | MISS dont_ship, MISS dont_ship, MISS dont_ship | ok escalate, ok escalate, ok escalate |
| e6 | ship | ok escalate, MISS None, ok escalate | ok ship (view escalate), ok ship (view escalate), ok ship (view escalate) |
| k1 | keep_running | ok keep_running, MISS cant_tell, MISS None | ok keep_running, ok keep_running, ok keep_running |
| k2 | keep_running | ok keep_running, ok keep_running, ok keep_running | ok keep_running, ok keep_running, ok keep_running |
| k3 | keep_running | MISS no_effect, MISS no_effect, MISS no_effect | ok keep_running, ok keep_running, ok keep_running |
| k4 | keep_running | ok keep_running, ok keep_running, ok keep_running | ok keep_running, ok keep_running, ok keep_running |
| n1 | no_effect | MISS dont_ship, MISS None, ok no_effect | ok no_effect, ok no_effect, ok no_effect |
| n2 | no_effect | ok no_effect, ok no_effect, ok no_effect | ok no_effect, ok no_effect, ok no_effect |
| n3 | no_effect | ok no_effect, ok no_effect, ok no_effect | ok no_effect, ok no_effect, ok no_effect |
| s1 | ship | ok ship, MISS dont_ship, ok ship | ok ship, ok ship, ok ship |
| s2 | ship | ok ship, ok ship, ok ship | ok ship, ok ship, ok ship |
| s3 | ship | ok ship, ok ship, ok ship | ok ship, ok ship, ok ship |
| s4 | ship | MISS None, ok ship, MISS dont_ship | ok ship, ok ship, ok ship |
| x1 | not_ab | MISS cant_tell, MISS None, ok not_ab | ok not_ab, ok not_ab, ok not_ab |
| x2 | not_ab | MISS keep_running, MISS dont_ship, MISS cant_tell | ok not_ab, ok not_ab, ok not_ab |
