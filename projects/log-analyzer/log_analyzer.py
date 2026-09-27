import sys
LEVELS = ["INFO", "WARNING", "ERROR"]
def count_log_levels(path):
    """
    Count the number of lines for each log level in a log file.

    Args:
        path (str): Path to the log file.

    Returns:
        dict: A dictionary with log levels as keys and their counts as values.
    """

    counts = {"Total lines": 0, "INFO": 0, "WARNING": 0, "ERROR": 0}
    
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():  # Only count non-empty lines
                counts["Total lines"] += 1
                for level in LEVELS:
                    if level in line:
                        counts[level] += 1
    return counts


def main():
    
    if len(sys.argv) == 1:
        print(f"Usage: {sys.argv[0]} <logfile>", file=sys.stderr)
        sys.exit(1)
    else:
        log_file_path = sys.argv[1]
        try:
            log_levels = count_log_levels(log_file_path)
            print(f"Log report: {log_file_path}")
            print("-" * 30)
            for level, count in log_levels.items():
                print(f"{level:<12}: {count}")
        except (FileNotFoundError, IsADirectoryError):
            print(f"Error: {log_file_path} does not exist or is not a regular file", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    main()
