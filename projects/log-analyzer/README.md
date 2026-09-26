# Log Analyzer

A small Bash tool that summarizes a log file: total entries and count per log level (INFO, WARNING, ERROR).

## Usage

```bash
./log_analyzer.sh <logfile>
```

Example:

```bash
./log_analyzer.sh samples/sample.log
```

```
Log report: samples/sample.log
------------------------------
Total lines : 10
INFO        : 5
WARNING     : 2
ERROR       : 3
```

## Behavior

- No argument: prints usage and exits with code 1.
- Path is missing or not a regular file: prints an error and exits with code 1.
- Empty lines are ignored in the total count.
- Error messages are written to stderr.

## Known limitations

- Log levels are matched anywhere in the line, so a message containing the word "ERROR" would be counted even if its level is INFO.
- Lines containing only spaces are counted as entries.
