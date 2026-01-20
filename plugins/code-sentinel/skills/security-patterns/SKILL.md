---
description: Security vulnerability patterns and detection rules
---

# Security Patterns Skill

## Critical Patterns (Always Block)

### SQL Injection
```python
# VULNERABLE
query = f"SELECT * FROM users WHERE id = {user_id}"
query = "SELECT * FROM users WHERE id = " + user_id

# SAFE
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
User.objects.filter(id=user_id)
```

### Command Injection
```python
# VULNERABLE
os.system(f"convert {filename} output.png")
subprocess.run(cmd, shell=True)

# SAFE
subprocess.run(["convert", filename, "output.png"], shell=False)
shlex.quote(filename)
```

### Code Injection
```python
# VULNERABLE
eval(user_input)
exec(user_code)

# SAFE
ast.literal_eval(user_input)  # Only for literals
# Use sandboxed execution environment
```

### XSS
```javascript
// VULNERABLE
element.innerHTML = userContent;
dangerouslySetInnerHTML={{__html: userData}}

// SAFE
element.textContent = userContent;
DOMPurify.sanitize(userContent)
```

### Hardcoded Secrets
```python
# VULNERABLE
API_KEY = "sk-1234567890abcdef"
password = "admin123"

# SAFE
API_KEY = os.environ.get("API_KEY")
password = get_secret("db_password")
```

### Unsafe Deserialization
```python
# VULNERABLE
data = pickle.loads(user_data)
config = yaml.load(file)  # yaml.load without Loader

# SAFE
data = json.loads(user_data)
config = yaml.safe_load(file)
```

## Warning Patterns (Flag but Allow)

### Broad Exception Handling
```python
# WARNING
try:
    risky_operation()
except:
    pass

# BETTER
try:
    risky_operation()
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    raise
```

### Missing Timeout
```python
# WARNING
response = requests.get(url)

# BETTER
response = requests.get(url, timeout=30)
```

### Path Traversal Risk
```python
# WARNING
file_path = os.path.join(base_dir, user_filename)

# BETTER
file_path = os.path.join(base_dir, os.path.basename(user_filename))
if not file_path.startswith(os.path.abspath(base_dir)):
    raise ValueError("Invalid path")
```
