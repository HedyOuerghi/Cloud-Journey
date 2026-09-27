# Log Analyzer

A small tool that summarizes a log file: total entries and count per log level (INFO, WARNING, ERROR). Implemented twice, in **Bash** and in **Python**, with identical behavior and output.

## Usage

```bash
./log_analyzer.sh <logfile>          # Bash version
python3 log_analyzer.py <logfile>    # Python version
```

Example:

```bash
python3 log_analyzer.py samples/sample.log
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
- Empty lines (including lines containing only whitespace) are ignored in the total count.
- Error messages are written to stderr.

## Files

| File | Description |
|------|-------------|
| `log_analyzer.sh` | Bash implementation (`grep`, `wc`, input validation) |
| `log_analyzer.py` | Python implementation (file reading, dictionary counting, `try/except`) |
| `samples/sample.log` | Example log file used for testing |

## Known limitations

- Log levels are matched anywhere in the line, so a message containing the word "ERROR" would be counted even if its level is INFO.
- Only supports a simple `date time LEVEL message` format. Other formats (syslog, web access logs, JSON logs) are not handled.
