# Onboarding

## Prerequisites

- Python 3.10+ (the standard library `unittest` module is used; no extra deps)

## Run the Tests

From the project root , run:

```bash
python -m unittest discover -s tests
```

This uses Python's built-in test discovery to execute all suites in `tests/`.

To run a single test file (for example `test_math_utils.py`), use:

```bash
python -m unittest tests.test_math_utils
```



