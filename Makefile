.PHONY: test fixtures hooks selftest eval grade

test:            ## unit tests (checks, parser, grader, guard, hook)
	python3 -m pytest -q

fixtures:        ## regenerate the synthetic fixtures and gold (deterministic)
	python3 eval/make_fixtures.py

hooks:           ## enable the denylist hook in this repo
	git config core.hooksPath .githooks

selftest:        ## safety-envelope self-test for the reference runner
	python3 safety/selftest.py

eval:            ## three arms x all fixtures x 3 runs (costs model usage)
	python3 eval/run_arms.py --runs 3 --model sonnet --parallel 6

grade:           ## make grade RUN=eval/results/<dir>
	python3 eval/grade.py $(RUN)
