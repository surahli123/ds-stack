meeting notes - how do we label relevance for the offline eval (oct 7)
attendees: eval team (4), search infra (2), me

context: we need ~6,000 query-result labels per quarter for the offline ndcg eval. today human raters do all of it via the vendor. it costs about $60k/quarter and turnaround is 3 weeks, which blocks ranker iterations.

option A - keep human raters as is. trusted, but slow and expensive. jamie pointed out raters disagree a lot on tail queries (agreement ~0.71).

option B - switch fully to an llm judge. we piloted it last month on 1,200 labels: agreement with the human majority label was 0.82 (cohen's kappa 0.74), cost would be ~$4k/quarter, turnaround same day. concern from priya: the judge drifts when the model version changes, we saw kappa drop to 0.61 after a provider update in the pilot. also legal hasn't approved sending query logs to the provider for all markets (EU is the blocker).

option C - hybrid: llm judge labels everything, humans label a 15% calibration sample every month (~900 labels) to measure drift, and humans do all EU queries. cost estimate ~$18k/quarter. turnaround 2 days for non-EU.

long discussion about whether kappa 0.74 is good enough. general sense: yes for ranking comparisons, not for absolute quality reporting to leadership.

we also talked about building our own fine-tuned judge, decided it's out of scope for this quarter.

what we agreed: recommend option C. need sign-off from the eval lead (morgan) on budget by oct 20 so we can cancel the vendor renewal before oct 31. risk to watch: judge drift - if monthly kappa on the calibration sample drops below 0.65 we fall back to humans for that month.
