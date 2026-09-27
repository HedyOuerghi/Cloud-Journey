import sys
import json
LEVELS = ["INFO", "WARNING", "ERROR"]
def count_log_levels(path):
    """
    Count the number of lines for each log level in a log file.

    Args:
        path (str): Path to the log file.

    Returns:
        dict: A dictionary with log levels as keys and their counts as values.
    """

    counts = {"total": 0, "INFO": 0, "WARNING": 0, "ERROR": 0}
    
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():  # Only count non-empty lines
                counts["total"] += 1
                for level in LEVELS:
                    if level in line:
                        counts[level] += 1
    return counts


def main():
    if len(sys.argv) == 2:
        json_output = False
    elif len(sys.argv) == 3 and sys.argv[2] == "--json":
        json_output = True
    else:
        print(f"Usage: {sys.argv[0]} <logfile> [--json]", file=sys.stderr)
        sys.exit(1)

    log_file_path = sys.argv[1]
    try:
        counts = count_log_levels(log_file_path)
    except (FileNotFoundError, IsADirectoryError):
        print(f"Error: '{log_file_path}' does not exist or is not a regular file", file=sys.stderr)
        sys.exit(1)

    if json_output:
        print(json.dumps(counts, indent=2))
    else:
        print(f"Log report: {log_file_path}")
        print("-" * 30)
        print(f"{'Total lines':<12}: {counts['total']}")
        for level in LEVELS:
            print(f"{level:<12}: {counts[level]}")

if __name__ == "__main__":
    main()
