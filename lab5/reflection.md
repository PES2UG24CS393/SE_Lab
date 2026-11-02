# Lab 5: Static Code Analysis — Reflection Report

**Student Name:** Rahul B  
**SRN:** PES2UG24CS393  
**Section:** G  
**Course:** Software Engineering Lab (UE23CS301)  
**Target File:** `tower_maintenance.py`  

---

### 1. Which issues were the easiest to fix, and which were the hardest? Why?

**Easiest Issues:**
The easiest issues to fix were the PEP 8 formatting warnings from Flake8 and Pylint. For example, Flake8 flagged that there were 3 blank lines before the `overdue` function instead of 2 (E303), and that `total=len(snapshot())` was missing spaces around the operator (E225). Breaking up long SQL query strings so they fit under 79 characters (E501) and writing docstrings for the module and each function was also very simple and mechanical because it didn't change any program logic.

**Hardest Issues:**
The hardest issues were:
1. Fixing the SQL injection vulnerability in `addTower` (Bandit B608). The original code used `%s` string interpolation inside the SQL string. I had to replace it with SQLite parameterized query placeholders `(?, ?, ?)` and pass the values as a tuple.
2. Handling the Bandit warning for `pickle` in `snapshot()` (B301/B403). The lab instructions specifically required keeping pickle. Bandit flags any use of pickle because loading untrusted data can lead to arbitrary code execution. I had to verify that our data was coming only from our own local in-memory SQLite table (meaning no untrusted user input), and add `# nosec` comments to document why it is safe here.
3. Fixing the broad exception in `serviceTower`. Replacing `except Exception:` with `except sqlite3.Error as exc:` and replacing the global `service_count` variable with a dictionary (`_service_state['count']`) required careful refactoring so Pylint wouldn't complain about global variables, while making sure the program output remained unchanged.

---

### 2. Did the static analysis tools report any false positives? If so, describe one example.

Yes, Bandit reported a clear false positive on line 6:
```python
NOC_PASSWORD = "tower-noc-77"
```
Bandit flagged this under `B105: Possible hardcoded password: 'tower-noc-77'`.

**Why it's a false positive:** Bandit uses pattern matching on variable names looking for words like 'password', 'token', or 'secret' assigned to a string literal. In this lab, `tower_maintenance.py` is an isolated prototype script that runs against an in-memory database (`:memory:`). There are no real servers, no network calls, and no real credentials involved. Treating this placeholder as a real security breach is a context-blind false positive. Even so, as a best practice, I changed it to read from an environment variable using `os.getenv('NOC_PASSWORD', '')`.

Another example was Bandit flagging `pickle.loads(pickle.dumps(records))` in `snapshot()`. Bandit treats all pickle deserialization as high risk, but in our script, the data was dumped directly from SQLite memory and reloaded in the exact same process. Because no external attacker could inject malicious bytes into the stream, there was no actual vulnerability.

---

### 3. How would you integrate static analysis tools into your actual software development workflow?

I would integrate static analysis tools into my development workflow in three places:

1. **Real-time Editor Linting (IDE):**
   Install Flake8 and Pylint extensions in VS Code so that syntax errors, formatting issues, and unused variables are highlighted with squiggles while typing. This catches small bugs before even saving the file.

2. **Git Pre-Commit Hooks:**
   Use the `pre-commit` framework (`.pre-commit-config.yaml`) to run Flake8, Bandit, and Pylint automatically whenever `git commit` is run. If there are any critical security vulnerabilities (like Bandit High/Medium) or syntax errors, the commit will be blocked locally until fixed.

3. **CI/CD Pipelines on GitHub / GitLab:**
   Add an automated workflow in GitHub Actions that runs on every Pull Request to `main`:
   - Run `flake8 .` to check code style.
   - Run `bandit -r .` to block security vulnerabilities.
   - Run `pylint` with a threshold (e.g., `--fail-under=9.0`).
   This ensures that no team member can merge broken or insecure code into the main codebase.

---

### 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

Applying the fixes produced clear, tangible improvements in the codebase:

1. **Security:**
   Parameterizing the SQL query in `addTower` removed the SQL injection vulnerability, ensuring that unexpected input strings cannot execute unintended SQL commands. Hardcoded passwords were also removed.

2. **Robustness:**
   Changing `except Exception:` to `except sqlite3.Error as exc:` in `serviceTower` means real runtime bugs (like NameErrors or keyboard interrupts) are no longer swallowed silently, and database errors print specific diagnostics.

3. **Readability and Style:**
   All lines are now within 79 characters, blank lines and spacing are consistent with PEP 8, and docstrings clearly explain the purpose, inputs, and outputs of every function.

4. **Measurable Results:**
   - Pylint score jumped from **5.14/10 to 10.00/10**.
   - Bandit issues dropped from **4 to 0**.
   - Flake8 errors dropped from **7 to 0**.
   - The script still prints `['Ridge-A'] high 2 1`, showing that the logic works exactly as intended.
