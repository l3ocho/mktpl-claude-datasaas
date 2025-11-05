# Hook Development Patterns

Comprehensive guide for creating event-driven automation with hooks.

## Hook Configuration

### Basic Structure
```json
{
  "hooks": [
    {
      "event": "file-changed",
      "pattern": "**/*.py",
      "script": "hooks/python_linter.sh"
    }
  ]
}
```

## Available Events

### file-changed
Triggered when files are modified in the workspace.

```json
{
  "event": "file-changed",
  "pattern": "**/*.{js,jsx,ts,tsx}",
  "script": "hooks/format_code.sh",
  "description": "Format JavaScript/TypeScript files"
}
```

**Event Data**:
- `CHANGED_FILE`: Path to modified file
- `FILE_EXTENSION`: File extension
- `PROJECT_ROOT`: Project root directory

### git-commit-msg-needed
Triggered when creating git commits.

```json
{
  "event": "git-commit-msg-needed",
  "script": "hooks/generate_commit_msg.py",
  "description": "Generate conventional commit messages"
}
```

**Event Data**:
- `STAGED_FILES`: List of staged files
- `DIFF_CONTENT`: Git diff content
- `BRANCH_NAME`: Current branch

### task-completed
Triggered after task completion.

```json
{
  "event": "task-completed",
  "pattern": "*deploy*",
  "script": "hooks/notify_team.sh",
  "description": "Notify team of deployment completion"
}
```

**Event Data**:
- `TASK_NAME`: Completed task name
- `TASK_DURATION`: Execution time
- `TASK_STATUS`: Success/failure

## Pattern Matching

### Glob Patterns
```json
{
  "pattern": "**/*.py",          // All Python files
  "pattern": "src/**/*.test.js", // Test files in src
  "pattern": "*.config.{js,json}", // Config files
  "pattern": "!**/*.min.js"      // Exclude minified
}
```

### Multiple Patterns
```json
{
  "event": "file-changed",
  "patterns": [
    "**/*.py",
    "**/*.pyi"
  ],
  "script": "hooks/python_type_check.sh"
}
```

### Regex Patterns
```json
{
  "event": "task-completed",
  "pattern_type": "regex",
  "pattern": "^deploy-.*-prod$",
  "script": "hooks/production_monitor.sh"
}
```

## Script Implementation

### Shell Script Example
```bash
#!/bin/bash
# hooks/format_code.sh

set -e

# Access event data
FILE_PATH="$CHANGED_FILE"
EXTENSION="$FILE_EXTENSION"

# Format based on file type
case "$EXTENSION" in
  js|jsx|ts|tsx)
    npx prettier --write "$FILE_PATH"
    ;;
  py)
    black "$FILE_PATH"
    ;;
  go)
    gofmt -w "$FILE_PATH"
    ;;
esac

echo "Formatted: $FILE_PATH"
```

### Python Script Example
```python
#!/usr/bin/env python3
# hooks/generate_commit_msg.py

import os
import json
import subprocess

def generate_commit_message():
    staged_files = os.environ.get('STAGED_FILES', '').split('\n')
    diff_content = os.environ.get('DIFF_CONTENT', '')
    
    # Analyze changes
    file_types = set()
    for file in staged_files:
        if file.endswith('.py'):
            file_types.add('python')
        elif file.endswith(('.js', '.tsx')):
            file_types.add('frontend')
    
    # Generate message
    if 'python' in file_types and 'frontend' in file_types:
        prefix = 'feat(fullstack):'
    elif 'python' in file_types:
        prefix = 'feat(backend):'
    else:
        prefix = 'feat(frontend):'
    
    return f"{prefix} Update {len(staged_files)} files"

if __name__ == "__main__":
    message = generate_commit_message()
    print(message)
```

### Node.js Script Example
```javascript
#!/usr/bin/env node
// hooks/validate_json.js

const fs = require('fs');
const path = require('path');

const filePath = process.env.CHANGED_FILE;

if (filePath.endsWith('.json')) {
  try {
    const content = fs.readFileSync(filePath, 'utf8');
    JSON.parse(content);
    console.log(`✓ Valid JSON: ${path.basename(filePath)}`);
  } catch (error) {
    console.error(`✗ Invalid JSON: ${filePath}`);
    console.error(error.message);
    process.exit(1);
  }
}
```

## Advanced Patterns

### Conditional Execution
```json
{
  "event": "file-changed",
  "pattern": "**/*.py",
  "script": "hooks/conditional_lint.sh",
  "conditions": {
    "branch_pattern": "feature/*",
    "skip_patterns": ["**/migrations/*"]
  }
}
```

### Chained Hooks
```json
{
  "hooks": [
    {
      "event": "file-changed",
      "pattern": "**/*.py",
      "script": "hooks/format.sh",
      "order": 1
    },
    {
      "event": "file-changed",
      "pattern": "**/*.py",
      "script": "hooks/lint.sh",
      "order": 2
    },
    {
      "event": "file-changed",
      "pattern": "**/*.py",
      "script": "hooks/type_check.sh",
      "order": 3
    }
  ]
}
```

### Debouncing
```json
{
  "event": "file-changed",
  "pattern": "**/*.scss",
  "script": "hooks/compile_sass.sh",
  "debounce": 1000,
  "description": "Compile SASS after 1s of no changes"
}
```

## Security Best Practices

### Input Validation
```bash
#!/bin/bash
# Validate file paths

FILE="$CHANGED_FILE"

# Check for directory traversal
if [[ "$FILE" == *".."* ]]; then
  echo "Error: Invalid file path"
  exit 1
fi

# Verify file exists in project
if [[ ! "$FILE" == "$PROJECT_ROOT"* ]]; then
  echo "Error: File outside project"
  exit 1
fi
```

### Safe Command Execution
```python
#!/usr/bin/env python3
import subprocess
import shlex
import os

def run_command_safely(cmd, file_path):
    # Sanitize file path
    safe_path = shlex.quote(file_path)
    
    # Use subprocess safely
    result = subprocess.run(
        [cmd, safe_path],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    return result.returncode == 0
```

### Environment Variable Safety
```bash
#!/bin/bash
# Sanitize environment variables

# Remove potentially dangerous characters
SAFE_BRANCH=$(echo "$BRANCH_NAME" | tr -cd '[:alnum:]/_-')

# Validate expected format
if [[ ! "$SAFE_BRANCH" =~ ^[a-zA-Z0-9/_-]+$ ]]; then
  echo "Error: Invalid branch name"
  exit 1
fi
```

## Performance Optimization

### Async Processing
```javascript
// hooks/async_process.js
const { Worker } = require('worker_threads');

async function processFileAsync(filePath) {
  return new Promise((resolve, reject) => {
    const worker = new Worker('./heavy_process.js', {
      workerData: { filePath }
    });
    
    worker.on('message', resolve);
    worker.on('error', reject);
  });
}
```

### Caching
```python
# hooks/cached_analysis.py
import hashlib
import json
import os

CACHE_DIR = os.path.join(os.environ['CLAUDE_PLUGIN_ROOT'], '.cache')

def get_file_hash(filepath):
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def get_cached_result(filepath):
    file_hash = get_file_hash(filepath)
    cache_file = os.path.join(CACHE_DIR, f"{file_hash}.json")
    
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            return json.load(f)
    return None
```

### Batch Processing
```bash
#!/bin/bash
# Process multiple files efficiently

# Collect files for batch processing
CHANGED_FILES=()
while read -r file; do
  CHANGED_FILES+=("$file")
done < <(echo "$STAGED_FILES")

# Process in batch
if [ ${#CHANGED_FILES[@]} -gt 10 ]; then
  echo "Batch processing ${#CHANGED_FILES[@]} files..."
  prettier --write "${CHANGED_FILES[@]}"
else
  # Process individually for small batches
  for file in "${CHANGED_FILES[@]}"; do
    prettier --write "$file"
  done
fi
```

## Testing Hooks

### Unit Testing
```python
# tests/test_hook.py
import unittest
import os
from hooks import generate_commit_msg

class TestCommitMsgHook(unittest.TestCase):
    def test_python_files(self):
        os.environ['STAGED_FILES'] = 'app.py\ntest.py'
        msg = generate_commit_msg.generate()
        self.assertIn('backend', msg)
```

### Integration Testing
```bash
#!/bin/bash
# test_hooks.sh

# Test file-changed hook
echo "Testing file-changed hook..."
touch test.py
CHANGED_FILE="test.py" FILE_EXTENSION="py" ./hooks/format_code.sh

# Verify result
if black --check test.py; then
  echo "✓ Hook executed successfully"
else
  echo "✗ Hook failed"
  exit 1
fi
```

## Troubleshooting

### Debug Mode
```json
{
  "event": "file-changed",
  "pattern": "**/*.py",
  "script": "hooks/lint.sh",
  "debug": true,
  "log_output": true
}
```

### Common Issues

1. **Hook not firing**
   - Check pattern matches
   - Verify event name
   - Ensure script is executable

2. **Script errors**
   - Add error handling
   - Check environment variables
   - Verify dependencies

3. **Performance issues**
   - Add debouncing
   - Implement caching
   - Use async processing

4. **Security warnings**
   - Validate all inputs
   - Use safe command execution
   - Restrict file access