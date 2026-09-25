# Bash — Notes

## Make a script executable and run it

```bash
chmod +x deploy.sh
./deploy.sh
```

**Notes:**

- `chmod +x deploy.sh` adds the execute permission to the file.
  - `+` **adds** a permission, `-` **removes** one.
  - `x` = *execute*.
  - Octal notation: `4` = read, `2` = write, `1` = execute (you add them up). E.g. `chmod 755` → `7` (rwx) for the owner, `5` (r-x) for the group, `5` for others.

- `./deploy.sh` runs the script. `./` specifies the **location** of the file — it does not execute it.
  - The shell looks for commands in the directories listed in `PATH` (`/usr/bin`, `/bin`, etc.). The current directory is not in there, for security reasons.
  - `./` = "in the current directory" (`.` = here). You explicitly tell the shell: the file is right here.

- **Key point — you need both:**
  - Without the execute permission → `permission denied` (fix it with `chmod +x`).
  - Without `./` (and outside PATH) → `command not found`.
  - `chmod +x` = the permission; `./` = the location.

## Count lines containing ERROR in a log

```bash
grep -c 'ERROR' /var/log/syslog
```

**Notes:**

- `grep` searches for a pattern (here `ERROR`) inside a file.
- The `-c` option (*count*) returns the **number** of matching lines directly, instead of printing the lines.

**Equivalent version using a pipe:**

```bash
grep 'ERROR' /var/log/syslog | wc -l
```

- The `|` (pipe) sends the **output** of the left-hand command as the **input** of the right-hand command.
- Here: `grep` outputs the lines containing `ERROR`, then `wc -l` counts those lines (`-l` = *lines*).
- Both versions give the same result; `grep -c` is just more direct.

## Inspecting logs: head, tail, tail -f

```bash
tail /var/log/syslog          # last 10 lines (default)
tail -n 20 /var/log/syslog    # last 20 lines
head /var/log/syslog          # first 10 lines
```

**Notes:**

- `head` = top = start of the file; `tail` = end of the file.
- Default: 10 lines. Use `-n NUMBER` (or `-NUMBER`) to choose another count. `-n` is the more explicit and more common form.

### Follow a log in real time

```bash
tail -f /var/log/syslog
```

- `-f` = *follow*: prints the end of the file **and stays open**, showing new lines as they are written.
- `Ctrl + C` to stop and regain control (works to interrupt any running command).

### Filter a live stream with pipes

```bash
tail -f /var/log/syslog | grep 'ERROR' | grep 'disk'
```

- The file goes on the command that reads it first (`tail`).
- After a pipe, `grep` takes **no** filename: it filters the stream received from the pipe.
- You can chain pipes: each `grep` narrows the stream down (here: lines with `ERROR`, then among those the ones with `disk`).

## find — searching for files

```bash
find /var/log -name "*.log"    # all .log files under /var/log (recursive)
find . -type d                 # all directories from here down
find . -type f                 # all regular files
```

**Structure:** `find [WHERE] [CRITERION] [ACTION]`
- WHERE: starting point, recursive by default
- `-name`: filter by name (`*` = wildcard)
- `-type d`: directories, `-type f`: regular files

**Why the quotes around `"*.log"`:**
- Without quotes, the shell performs *globbing*: it replaces `*.log` with the matching files in the current directory **before** `find` even runs.
- `find` then receives several names instead of a single pattern → error, and behavior that changes depending on the directory's contents.
- Quotes stop the shell from touching the `*`: the raw pattern is passed to `find`, which handles the search itself. Reliable behavior everywhere.