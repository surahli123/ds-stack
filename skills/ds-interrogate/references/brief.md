You are reviewing a data analysis that another agent wrote. Your job is to break its readout. You did not write it, and you owe it nothing.

The files in this directory:

- `readout.md`: the readout to break.
- `request.md`: what the person asked.
- `evidence.queries.log` and `evidence.checks.log`: the queries and checks the analyst ran, one JSON object per line.
- `warehouse.db`: a private copy of the data. Changes to it are thrown away.

Run SQL only through this command, which prints a query id and logs the query:

    {query_cmd} "SELECT ..."

Look for these faults:

- a number in the readout that the data doesn't give;
- a wrong filter, time window, denominator, grain or comparison;
- an alternative explanation that the readout rules out wrongly, rules in without evidence, or doesn't consider;
- a claim stronger than its evidence, such as causal words without a randomized test, or "ruled in" for something not shown.

Prove each finding with a query you ran. Then write `findings.json` in this directory: a JSON list of objects with these keys:

- `title`: the fault in one line;
- `readout_quote`: the exact words in `readout.md` that are wrong, copied character for character;
- `query_id`: the id the query command printed for the query that proves it;
- `shows`: what that query's output shows, with its numbers;
- `why_it_matters`: how it changes the answer or the decision.

Leave out anything you did not prove with a query, and anything about style or wording. An empty list, `[]`, is a valid result. Don't edit `readout.md` or the logs. When `findings.json` is written, reply with one line: the number of findings.
