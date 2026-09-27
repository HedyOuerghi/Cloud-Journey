import sys

def count_errors(path):
    """
    Count the number of lines containing ERROR in a log file.

    Args:
        path (str): Path to the log file.

    Returns:
        int: Number of matching lines.
    """
    count = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            if "ERROR" in line:
                count += 1
    return count


paths = [
    "../projects/log-analyzer/samples/sample.log",
    "../projects/log-analyzer/samples/nope.log",
    "../projects/log-analyzer/samples/sample.log",
]

for p in paths:
    try:
        print(p, count_errors(p))
    except FileNotFoundError:
        print(f"Error: file not found: {p}", file=sys.stderr)