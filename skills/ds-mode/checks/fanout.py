"""Catch joins that silently add or lose rows.

Pass the row counts around a join. Fails when the right side has duplicate keys
for a join meant to be many-to-one or one-to-one, when the join added rows, or
when a left join lost rows. An inner join that drops rows passes with the drop
reported, unless it exceeds `max_drop_fraction`.
"""

from _common import COULD_NOT_RUN, FAIL, PASS, Result, SpecError, require

NAME = "fanout"
RELATIONSHIPS = {"many_to_one", "one_to_one"}
JOINS = {"left", "inner"}


def run(spec):
    try:
        left_rows = require(spec, "left_rows", int)
        joined_rows = require(spec, "joined_rows", int)
        relationship = spec.get("relationship", "many_to_one")
        join = spec.get("join", "left")
        if relationship not in RELATIONSHIPS:
            raise SpecError(f"'relationship' must be one of {sorted(RELATIONSHIPS)}")
        if join not in JOINS:
            raise SpecError(f"'join' must be one of {sorted(JOINS)}")
        right_rows = spec.get("right_rows")
        right_keys = spec.get("right_distinct_keys")
        if (right_rows is None) != (right_keys is None):
            raise SpecError("pass both 'right_rows' and 'right_distinct_keys', or neither")
        if right_rows is not None:
            right_rows = require(spec, "right_rows", int)
            right_keys = require(spec, "right_distinct_keys", int)
        max_drop = spec.get("max_drop_fraction")
    except (SpecError, TypeError, ValueError) as err:
        return Result(NAME, COULD_NOT_RUN, f"could not run: {err}")

    details = {"left_rows": left_rows, "joined_rows": joined_rows,
               "relationship": relationship, "join": join}
    problems = []
    if right_rows is not None:
        details.update(right_rows=right_rows, right_distinct_keys=right_keys)
        if right_rows > right_keys:
            problems.append(
                f"right side has {right_rows - right_keys} duplicate-key rows "
                f"({right_rows} rows for {right_keys} keys); dedupe or filter before joining"
            )
    if joined_rows > left_rows:
        problems.append(f"join added {joined_rows - left_rows} rows (fan-out)")
    dropped = left_rows - joined_rows if joined_rows < left_rows else 0
    if dropped:
        fraction = dropped / left_rows
        details["dropped_rows"] = dropped
        details["dropped_fraction"] = round(fraction, 6)
        if join == "left":
            problems.append(f"left join lost {dropped} rows; the query is not the join you think")
        elif max_drop is not None and fraction > float(max_drop):
            problems.append(f"inner join dropped {fraction:.1%} of rows (limit {float(max_drop):.1%})")

    if problems:
        return Result(NAME, FAIL, "; ".join(problems), details)
    note = f"; inner join dropped {dropped} rows" if dropped else ""
    return Result(NAME, PASS, f"row counts consistent with a {relationship} {join} join{note}", details)
