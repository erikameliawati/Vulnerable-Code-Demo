# Security Vulnerabilities Demo

## What the Script Does

The scripts demonstrate two critical security vulnerabilities:

1. **SQL Injection**: Allows attackers to manipulate database queries
2. **Command Injection**: Allows attackers to execute arbitrary system commands

The script is interactive - we can input data manually to see how attacks work in real-time.

## Prerequisites

- Python 3.6 or higher
- No external dependencies required (uses only standard library)

## Installation

1. Download the Python file:
   - `vulnerable_script.py`

2. No installation needed - just run the scripts directly

## How to Run the Script

```bash
python vulnerable_script.py
```

**Menu Options:**
1. SQL Injection Demo
2. Command Injection Demo
3. Exit

## Vulnerabilities Demonstrated

### 1. SQL Injection

A code injection technique where attackers insert malicious SQL code into application queries, allowing them to bypass authentication, access unauthorized data, or manipulate the database.

**How to test it:**

In `vulnerable_script.py`:
- Choose option 1 (SQL Injection Demo)
- Try these credentials:
  - Username: `admin' --`
  - Password: `anything`
- Result: You'll bypass authentication and login as admin!

**Why it's vulnerable:**
```python
# Vulnerable code
query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
cursor.execute(query)
```

The user input is directly concatenated into the SQL query, allowing attackers to inject SQL code.

**The fix:**
```python
# Secure code
query = "SELECT * FROM users WHERE username=? AND password=?"
cursor.execute(query, (username, password))
```

Uses parameterized queries where the database driver automatically escapes special characters.

### 2. Command Injection

A vulnerability that allows attackers to execute arbitrary operating system commands on the server by injecting malicious input into system command calls.

**How to test it:**

In `vulnerable_script.py`:
- Choose option 2 (Command Injection Demo)
- Try these inputs:
  - **Windows**: `document.txt & whoami`
  - **Linux/Mac**: `document.txt; whoami`
- Result: Both commands execute - the file listing AND the whoami command!

**Why it's vulnerable:**
```python
# Vulnerable code - Windows
command = f"dir {filename}"
os.system(command)
```

User input is directly inserted into a system command without validation, allowing shell metacharacters like `&`, `;`, `|`, `&&` to execute additional commands.

**The fix:**
```python
# Secure code
# 1. Validate input
allowed_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-")
if not all(c in allowed_chars for c in filename):
    print("Invalid filename!")
    return

# 2. Use subprocess with argument list
subprocess.run(['cmd', '/c', 'dir', filename], capture_output=True)
```

The secure version:
- Validates input to only allow safe characters
- Uses `subprocess.run()` with a list of arguments instead of `os.system()`
- Avoids shell interpretation of special characters

## Attack Examples

### SQL Injection Attacks to Try

| Attack | Description |
|--------|-------------|
| `admin' --` | Comments out the password check |
| `admin' OR '1'='1` | Always true condition |
| `' OR '1'='1' --` | Bypasses both username and password |

### Command Injection Attacks to Try

**Windows:**
| Attack | Description |
|--------|-------------|
| `document.txt & whoami` | Execute multiple commands |
| `document.txt && echo Hacked!` | Chain commands |
| `document.txt & type document.txt` | Read file contents |

**Linux/Mac:**
| Attack | Description |
|--------|-------------|
| `document.txt; whoami` | Execute multiple commands |
| `document.txt && echo 'Hacked!'` | Chain commands |
| `document.txt \| cat /etc/passwd` | Pipe to another command |

## Security Remediations Summary

| Vulnerability | Vulnerable Practice | Secure Practice |
|---------------|---------------------|-----------------|
| SQL Injection | String concatenation in queries | Parameterized queries with placeholders |
| Command Injection | `os.system()` with user input | `subprocess.run()` with argument list + input validation |

