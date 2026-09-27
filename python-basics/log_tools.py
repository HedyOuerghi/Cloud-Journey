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


if len(sys.argv) == 1:
    print(f"Usage: {sys.argv[0]} <logfile>", file=sys.stderr)
    sys.exit(1)
else:
    log_file_path = sys.argv[1]
    try:
        print(f"{log_file_path}: {count_errors(log_file_path)} errors")
    except FileNotFoundError:
        print(f"Error: file not found: {log_file_path}", file=sys.stderr)
        sys.exit(1)
