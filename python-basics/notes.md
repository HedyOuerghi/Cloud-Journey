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
