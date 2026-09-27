# Python - Notes

## Context

I studied Python in high school (NSI, computer science specialty) and during my two years of CPGE (French intensive preparatory classes for engineering schools). This section is a structured refresher: re-checking the fundamentals I use, making sure I understand *why* Python behaves the way it does, and filling the gaps before moving on to cloud automation (files, JSON, APIs, `boto3`).

## Types and operators

The same operator behaves differently depending on the types involved.

```python
"5" * 3      # '555'  -> string repetition
"5" + 3      # TypeError -> Python won't add text and a number
int("5") + 3 # 8
```

## range

`range(start, stop)` stops **before** `stop`.

```python
for i in range(1, 6):
    print(i)   # 1, 2, 3, 4, 5
```

`range(6)` starts at 0: `0, 1, 2, 3, 4, 5`.

## Dictionaries

```python
server = {"name": "web-01", "region": "eu-west-3", "cpu": 2}

server["region"]    # 'eu-west-3'
server["ram"]       # KeyError: reading a missing key does NOT create it
server["ram"] = 4   # a key is added only by assignment
```

## f-strings

Everything inside `{}` is evaluated, including expressions.

```python
name = "Hedy"
print(f"Hello {name}, you have {2 + 3} messages")
# Hello Hedy, you have 5 messages
```

## Names are labels, not boxes

A variable is a label attached to an object in memory. Assignment never copies: it attaches another label to the **same** object.

```python
a = [1, 2, 3]
b = a          # b and a point to the same list
b.append(4)
print(a)       # [1, 2, 3, 4]

b = a.copy()   # a real copy: a new list
```

`id(obj)` returns the object's identity: two labels on the same object share the same `id`.

## Mutable vs immutable

- **Immutable:** the object can never change. Any "modification" creates a new object.
- **Mutable:** the object can be changed in place, and every label pointing to it sees the change.

| Immutable | Mutable |
|---|---|
| `int`, `float`, `bool` | `list` |
| `str` | `dict` |
| `tuple` | `set` |
| `None` | |

Mutable means the object **can** be modified in place, not that every operation does it:

| Modifies in place | Creates a new object |
|---|---|
| `a.append(x)` | `a + [x]` |
| `a.remove(x)` | `sorted(a)` |
| `a.sort()` | `a.copy()` |
| `a[0] = x`, `d["key"] = v` | `a[1:3]` (slice) |

```python
a = [1, 2]
b = a
b = b + [3]   # new list, then b is re-attached to it
print(a)      # [1, 2]
```

### Strings are immutable

String methods never modify the string, they **return** a new one.

```python
s = "hello"
s.upper()      # new string created and thrown away
print(s)       # hello
s = s.upper()  # keep the result
print(s)       # HELLO
```

## Functions and mutability

A function receives a label on the **same** object as the caller.

```python
def add_env(config):
    config["env"] = "prod"     # modifies the dict in place

server = {"name": "web-01"}
add_env(server)
print(server)   # {'name': 'web-01', 'env': 'prod'}
```

```python
def add_one(n):
    n = n + 1       # re-attaches the local label n, caller unaffected

x = 5
add_one(x)
print(x)        # 5
```

**Rule:** a function can change what you pass it **only if** the object is mutable **and** the function modifies it in place. Re-assigning the parameter (`param = ...`) never affects the caller. Same behavior as Java with objects vs primitives.

## Reading files

```python
with open(path, encoding="utf-8") as f:
    for line in f:
        ...
```

- `with` closes the file automatically at the end of the block, even if an error occurs.
- Iterating over the file object reads it **line by line** (each line ends with `\n`).
- `encoding="utf-8"` makes the behavior identical on every machine.
- `"ERROR" in line` tests whether a string contains another one.

## Reading a traceback

Read it **from the bottom**: the last line gives the error type (e.g. `FileNotFoundError`) and its message. The lines above show the call chain, from the outermost call to where the error was raised.

## Handling errors: try / except

```python
import sys

def count_errors(path):
    count = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            if "ERROR" in line:
                count += 1
    return count

for p in paths:
    try:
        print(p, count_errors(p))
    except FileNotFoundError:
        print(f"Error: file not found: {p}", file=sys.stderr)
```

- **Catch a specific exception**, never a bare `except:` (or a broad `except Exception`): it would also hide bugs in your own code.
- **Handle errors where the decision belongs.** The function's job is to count; it lets the error propagate. The caller decides what to do: skip the file and continue, or stop everything with `sys.exit(1)`.
- **Never hide a failure behind a default value.** Returning `0` for a missing file would make "no errors" and "could not read the file" look identical.
- Errors go to **stderr**: `print(..., file=sys.stderr)`. Exit code: `sys.exit(1)`. Same conventions as in Bash (`>&2`, `exit 1`).

## Command-line arguments: sys.argv

```python
import sys

if len(sys.argv) == 1:
    print(f"Usage: {sys.argv[0]} <logfile>", file=sys.stderr)
    sys.exit(1)

log_file_path = sys.argv[1]
try:
    print(f"{log_file_path}: {count_errors(log_file_path)} errors")
except FileNotFoundError:
    print(f"Error: file not found: {log_file_path}", file=sys.stderr)
    sys.exit(1)
```

- `sys.argv` is a list of what was typed on the command line. The script name is **always** included.

| Bash | Python |
|---|---|
| `$0` | `sys.argv[0]` |
| `$1` | `sys.argv[1]` |
| `$#` | `len(sys.argv) - 1` |

- With no argument, `sys.argv` is `['script.py']` (length 1): accessing `sys.argv[1]` raises `IndexError`. Always check the length first.
- A `try` only protects the code written **inside** it: the call that can fail must be in the block.
- Writing to stderr does **not** change the exit code. On failure, call `sys.exit(1)` explicitly, otherwise the script returns 0 and is seen as successful. A script that ends normally returns 0.


## JSON

JSON is a **text** format for structured data, used everywhere in the cloud (API responses, configs, AWS IAM policies, structured logs).

| JSON | Python |
|---|---|
| object `{"key": value}` | `dict` |
| array `[1, 2]` | `list` |
| string `"text"` | `str` |
| number | `int`, `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

Rules: strings and keys always in **double quotes**, keys are always strings, no trailing comma.

```python
import json

text = json.dumps(data, indent=2)   # Python object -> JSON text
data = json.loads(text)             # JSON text -> Python object

with open("report.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)    # write directly to a file
with open("report.json", encoding="utf-8") as f:
    data = json.load(f)             # read directly from a file
```

- The `s` in `dumps` / `loads` stands for **string**.
- A JSON string is **not** a dict: `text["key"]` makes no sense. Work with Python objects in memory, convert to JSON to exchange or store.
- `open(..., "w")` writes and overwrites (like `>`), `"a"` appends (like `>>`), default `"r"` reads.

## Short-circuit evaluation

```python
elif len(sys.argv) == 3 and sys.argv[2] == "--json":
```

`and` stops as soon as the left side is `False`: `sys.argv[2]` is never read when it does not exist. Put the guarding check **first**. Same principle as `&&` in Bash.
