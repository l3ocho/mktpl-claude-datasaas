# Performance Optimization Guide

Comprehensive guide for optimizing Claude plugin performance.

## Startup Performance

### Lazy Loading
```json
// plugin.json
{
  "config": {
    "lazy_load": true,
    "preload_commands": ["help", "version"],
    "defer_agents": true
  }
}
```

### Minimal Dependencies
```python
# ❌ Bad: Import everything upfront
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests

# ✅ Good: Import when needed
def analyze_data(file_path):
    import pandas as pd  # Import only when function is called
    return pd.read_csv(file_path)
```

### Command Organization
```
# ❌ Bad: Many small files
commands/
├── create-user.md
├── delete-user.md
├── update-user.md
├── list-users.md
└── ... (20 more files)

# ✅ Good: Grouped commands
commands/
├── user/
│   ├── create.md
│   ├── delete.md
│   ├── update.md
│   └── list.md
└── _index.md
```

## Command Execution

### Async Operations
```python
#!/usr/bin/env python3
# scripts/async_deploy.py

import asyncio
import aiohttp
import aiofiles

async def deploy_services(services):
    """Deploy multiple services concurrently."""
    tasks = [deploy_single(service) for service in services]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for service, result in zip(services, results):
        if isinstance(result, Exception):
            print(f"Failed to deploy {service}: {result}")
        else:
            print(f"Successfully deployed {service}")

async def deploy_single(service):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"https://api.deploy.com/{service}") as resp:
            return await resp.json()
```

### Caching Strategies
```python
# scripts/cached_operations.py

import functools
import time
import json
from pathlib import Path

CACHE_DIR = Path("${CLAUDE_PLUGIN_ROOT}/.cache")
CACHE_DIR.mkdir(exist_ok=True)

def timed_cache(seconds=300):
    """Cache function results for specified seconds."""
    def decorator(func):
        cache = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__name__}:{args}:{kwargs}"
            now = time.time()
            
            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < seconds:
                    return result
            
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result
        
        return wrapper
    return decorator

@timed_cache(seconds=600)
def expensive_api_call(endpoint):
    """Cached API call - results valid for 10 minutes."""
    # Implementation
    pass
```

### Stream Processing
```bash
#!/bin/bash
# hooks/process_large_file.sh

# ❌ Bad: Load entire file
content=$(cat "$LARGE_FILE")
processed=$(echo "$content" | process_command)

# ✅ Good: Stream processing
process_command < "$LARGE_FILE" > "$OUTPUT_FILE"

# For line-by-line processing
while IFS= read -r line; do
    process_line "$line"
done < "$LARGE_FILE"
```

## Memory Management

### Resource Cleanup
```python
# scripts/resource_manager.py

import contextlib
import tempfile
import shutil

@contextlib.contextmanager
def temp_workspace():
    """Create temporary workspace that's automatically cleaned up."""
    temp_dir = tempfile.mkdtemp(prefix="claude_plugin_")
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

# Usage
def process_files(files):
    with temp_workspace() as workspace:
        # All files in workspace are automatically deleted
        for file in files:
            process_in_workspace(file, workspace)
```

### Efficient Data Structures
```python
# ❌ Bad: Multiple passes over data
def analyze_logs(log_file):
    lines = open(log_file).readlines()
    
    error_count = sum(1 for line in lines if "ERROR" in line)
    warning_count = sum(1 for line in lines if "WARNING" in line)
    info_count = sum(1 for line in lines if "INFO" in line)

# ✅ Good: Single pass
def analyze_logs(log_file):
    counts = {"ERROR": 0, "WARNING": 0, "INFO": 0}
    
    with open(log_file) as f:
        for line in f:
            for level in counts:
                if level in line:
                    counts[level] += 1
                    break
    
    return counts
```

### Generator Functions
```python
# scripts/data_processor.py

def process_large_dataset(file_path):
    """Process large dataset using generators."""
    def read_chunks(file, chunk_size=1024*1024):
        """Read file in chunks to avoid memory issues."""
        with open(file, 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                yield chunk
    
    for chunk in read_chunks(file_path):
        process_chunk(chunk)
```

## Hook Performance

### Debouncing File Changes
```javascript
// hooks/debounced_compiler.js

const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

const compileStyles = debounce(() => {
    console.log('Compiling styles...');
    // Compilation logic
}, 1000);

// File change handler
process.env.CHANGED_FILE && compileStyles(process.env.CHANGED_FILE);
```

### Selective Processing
```bash
#!/bin/bash
# hooks/smart_formatter.sh

# Only process changed parts
if command -v git >/dev/null 2>&1; then
    # Get only modified lines
    git diff --unified=0 "$CHANGED_FILE" | \
    grep -E '^\+[^+]' | \
    sed 's/^+//' > changed_lines.tmp
    
    # Process only changed content
    format_lines < changed_lines.tmp
else
    # Fallback to full file
    format_file "$CHANGED_FILE"
fi
```

## Network Optimization

### Connection Pooling
```python
# scripts/api_client.py

import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

class OptimizedAPIClient:
    def __init__(self):
        self.session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        # Configure connection pooling
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=20
        )
        
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
    
    def get(self, url, **kwargs):
        return self.session.get(url, **kwargs)

# Global client instance
api_client = OptimizedAPIClient()
```

### Parallel Downloads
```python
# scripts/parallel_downloader.py

import asyncio
import aiohttp
import aiofiles
from pathlib import Path

async def download_files(urls, output_dir, max_concurrent=5):
    """Download multiple files concurrently."""
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)
    
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def download_one(session, url):
        async with semaphore:
            filename = output_dir / Path(url).name
            async with session.get(url) as response:
                async with aiofiles.open(filename, 'wb') as f:
                    async for chunk in response.content.iter_chunked(8192):
                        await f.write(chunk)
            return filename
    
    async with aiohttp.ClientSession() as session:
        tasks = [download_one(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

## Profiling & Monitoring

### Performance Metrics
```python
# scripts/performance_monitor.py

import time
import functools
import json
from datetime import datetime

METRICS_FILE = "${CLAUDE_PLUGIN_ROOT}/.metrics.json"

def track_performance(func):
    """Decorator to track function performance."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        # Record metrics
        metrics = {
            "function": func.__name__,
            "duration": end_time - start_time,
            "timestamp": datetime.now().isoformat(),
            "args_size": len(str(args)),
            "result_size": len(str(result))
        }
        
        # Append to metrics file
        with open(METRICS_FILE, 'a') as f:
            json.dump(metrics, f)
            f.write('\n')
        
        return result
    return wrapper
```

### Memory Profiling
```python
# scripts/memory_profiler.py

import tracemalloc
import functools

def profile_memory(func):
    """Profile memory usage of a function."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tracemalloc.start()
        
        result = func(*args, **kwargs)
        
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        print(f"{func.__name__} memory usage:")
        print(f"  Current: {current / 1024 / 1024:.2f} MB")
        print(f"  Peak: {peak / 1024 / 1024:.2f} MB")
        
        return result
    return wrapper
```

## Best Practices

### 1. Measure Before Optimizing
```bash
# Time command execution
time claude /my-plugin slow-command

# Profile Python scripts
python -m cProfile -s cumtime scripts/my_script.py

# Memory usage
/usr/bin/time -v claude /my-plugin memory-heavy-command
```

### 2. Progressive Enhancement
```json
// plugin.json
{
  "features": {
    "basic": ["core-command"],
    "enhanced": ["advanced-features"],
    "premium": ["ai-powered-analysis"]
  },
  "config": {
    "feature_detection": true,
    "fallback_mode": "basic"
  }
}
```

### 3. Resource Limits
```python
# scripts/resource_limited.py

import resource
import signal

def limit_resources():
    """Set resource limits for safety."""
    # Limit memory to 1GB
    resource.setrlimit(
        resource.RLIMIT_AS,
        (1024 * 1024 * 1024, 1024 * 1024 * 1024)
    )
    
    # Limit CPU time to 60 seconds
    resource.setrlimit(
        resource.RLIMIT_CPU,
        (60, 60)
    )
    
    # Set timeout handler
    def timeout_handler(signum, frame):
        raise TimeoutError("Operation timed out")
    
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(60)

# Use in scripts
if __name__ == "__main__":
    limit_resources()
    main()
```

### 4. Efficient File Operations
```python
# scripts/efficient_file_ops.py

import mmap
import os

def search_in_large_file(file_path, search_term):
    """Search in large files using memory mapping."""
    with open(file_path, 'rb') as f:
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mmapped:
            search_bytes = search_term.encode()
            position = mmapped.find(search_bytes)
            
            if position != -1:
                # Found - extract context
                start = max(0, position - 100)
                end = min(len(mmapped), position + 100)
                context = mmapped[start:end].decode('utf-8', errors='ignore')
                return context
    
    return None
```

## Performance Checklist

- [ ] Commands load in < 100ms
- [ ] Startup time < 500ms
- [ ] Memory usage < 100MB for basic operations
- [ ] No blocking operations in main thread
- [ ] Proper cleanup of temporary files
- [ ] Connection pooling for network requests
- [ ] Caching for expensive operations
- [ ] Progressive loading of features
- [ ] Resource limits configured
- [ ] Performance metrics tracked