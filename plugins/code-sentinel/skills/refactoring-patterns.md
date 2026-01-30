---
description: Code refactoring patterns and techniques for improving structure and maintainability
---

# Refactoring Patterns Skill

## Structure Patterns

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| `extract-method` | Extract code block into named function | Long functions, repeated logic |
| `extract-class` | Move related methods to new class | Class doing too much |
| `inline` | Inline trivial function/variable | Over-abstracted code |
| `rename` | Rename with all references updated | Unclear naming |
| `move` | Move function/class to different module | Misplaced code |

### extract-method Example
```python
# BEFORE
def process_order(order):
    # Validate (extract this)
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")
    # Process
    for item in order.items:
        inventory.reserve(item)
    return create_invoice(order)

# AFTER
def validate_order(order):
    if not order.items:
        raise ValueError("Empty order")
    if order.total < 0:
        raise ValueError("Invalid total")

def process_order(order):
    validate_order(order)
    for item in order.items:
        inventory.reserve(item)
    return create_invoice(order)
```

## Simplification Patterns

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| `simplify-conditional` | Flatten nested if/else | Deep nesting (>3 levels) |
| `remove-dead-code` | Delete unreachable code | After refactoring |
| `consolidate-duplicate` | Merge duplicate code blocks | DRY violations |
| `decompose-conditional` | Break complex conditions into named parts | Long boolean expressions |

### simplify-conditional Example
```python
# BEFORE
if user:
    if user.active:
        if user.has_permission:
            do_action()

# AFTER (guard clauses)
if not user:
    return
if not user.active:
    return
if not user.has_permission:
    return
do_action()
```

## Modernization Patterns

| Pattern | Description | When to Use |
|---------|-------------|-------------|
| `use-comprehension` | Convert loops to list/dict comprehensions | Simple transformations |
| `use-pathlib` | Replace os.path with pathlib | File path operations |
| `use-fstring` | Convert .format() to f-strings | String formatting |
| `use-typing` | Add type hints | Public APIs, complex functions |
| `use-dataclass` | Convert class to dataclass | Data-holding classes |

### use-dataclass Example
```python
# BEFORE
class User:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age

# AFTER
@dataclass
class User:
    name: str
    email: str
    age: int
```

## Code Smell Detection

| Smell | Indicators | Suggested Pattern |
|-------|------------|-------------------|
| Long Method | >20 lines, multiple responsibilities | extract-method |
| Large Class | >10 methods, low cohesion | extract-class |
| Primitive Obsession | Many related primitives | use-dataclass |
| Nested Conditionals | >3 nesting levels | simplify-conditional |
| Duplicate Code | Copy-pasted blocks | consolidate-duplicate |
| Dead Code | Unreachable branches | remove-dead-code |

## Metrics

After refactoring, measure improvement:

| Metric | Good Target | Tool |
|--------|-------------|------|
| Cyclomatic Complexity | <10 per function | radon, lizard |
| Function Length | <25 lines | manual count |
| Class Cohesion | LCOM <0.5 | pylint |
| Duplication | <3% | jscpd, radon |
