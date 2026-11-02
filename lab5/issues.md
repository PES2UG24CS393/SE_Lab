# Static Code Analysis Issues Log — Telecom Tower Maintenance Tracker

**Student Name:** Rahul B  
**SRN:** PES2UG24CS393  
**Section:** G  
**Target File:** `tower_maintenance.py`  

---

## Documented Issues Table

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| **SQL Injection Vector (B608)** | Security (Bandit) — Medium Severity | 11 | String interpolation `%s` used to construct SQL query inside `addTower`, introducing SQL injection vulnerability (CWE-89). | Replace Python `%` string formatting with DB-API parameterized query syntax `(?, ?, ?)`. |
| **Pickle Deserialization of Data (B301 / B403)** | Security (Bandit) — Medium / Low Severity | 1, 43 | `pickle.loads` / `dumps` used in `snapshot()`. Pickle can be unsafe when deserializing untrusted data (CWE-502). | Keep `pickle` as required by assignment specification for serialization, and annotate with `# nosec B301, B403` documenting the local in-memory context. |
| **Hardcoded Password String (B105)** | Security (Bandit) — Low Severity | 6 | Plaintext mock secret `NOC_PASSWORD = "tower-noc-77"` hardcoded at module level (CWE-259). | Retrieve credential dynamically from environment variable via `os.getenv("NOC_PASSWORD", "")` rather than hardcoding. |
| **Broad Exception Catching (W0718)** | Code Quality (Pylint) — Warning | 20 | Catches generic `Exception` in `serviceTower`, which masks unexpected errors and prevents debugging. | Narrow the exception catch clause to specific database errors (`sqlite3.Error`) and log the exception details. |
| **Global Mutable State (W0603 / C0103)** | Architecture / Quality (Pylint) — Warning | 7, 16 | Lowercase global variable `service_count` modified inside `serviceTower` using the `global` statement. | Encapsulate mutable state in a dictionary or structured container (`_service_state["count"]`) without requiring `global`. |
| **Missing Module & Function Docstrings (C0114 / C0116)** | Code Quality (Pylint) — Convention | 1, 10, 15, 25, 34, 42, 46 | Missing docstrings for module and functions `addTower`, `serviceTower`, `overdue`, `riskLevel`, `snapshot`, `main`. | Add descriptive PEP 257 docstrings explaining purpose, parameters, and return types for the module and all functions. |
| **PEP 8 Line Length Exceeded (E501 / C0301)** | Style (Flake8 / Pylint) — Style Violation | 5, 11, 18, 35, 43 | Multiple SQL query strings and statements exceed the 79/100 character maximum limit. | Wrap queries across multiple clean lines using implicit string continuation. |
| **PEP 8 Whitespace & Blank Lines (E303 / E225)** | Style (Flake8) — Style Violation | 25, 50 | 3 blank lines before `overdue` (PEP 8 expects 2); missing whitespace around operator in `total=len(...)`. | Reduce blank lines to 2 and format assignment with whitespace (`total = len(...)`). |
| **Unnecessary Else After Return (R1705)** | Code Quality (Pylint) — Refactor | 36-39 | In `riskLevel`, `else` branch is unnecessary after explicit `return "high"`. | Remove the `else` clause and de-indent `return "normal"`. |
