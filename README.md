# unused-import

A small, dependency-free Python CLI that finds **unused imports** in Python source files
using the standard-library `ast` module. No external tools, no config, no network access.

## Features

- Static analysis via `ast` — no import execution, safe on untrusted code.
- Reports file, line number, imported name, and origin module.
- Skips common noise directories (`.git`, `venv`, `__pycache__`, …).
- `--json` output for CI integration.
- Non-zero exit code when unused imports are found (great for pre-commit / CI gates).
- Handles `import x`, `import x as y`, `from x import y`, `from x import y as z`, and `*` (ignored).
- Respects `__all__` declarations (names listed there count as used).

## Install

No installation required beyond Python 3.9+.

```bash
git clone https://github.com/yourname/unused-import.git
cd unused-import
chmod +x unused_import.py
```

Or copy `analyzer.py` and `unused_import.py` anywhere on your `PATH`.

## Usage

Scan the current directory:

```bash
python3 unused_import.py
```

Scan specific files or directories:

```bash
python3 unused_import.py src/ tests/ main.py
```

JSON output:

```bash
python3 unused_import.py --json
```

Example output:

```
src/app.py:3: unused import 'os' (os)
src/app.py:7: unused import 'json' (json)
```

### Exit codes

- `0` — no unused imports found.
- `1` — at least one unused import found.
- `2` — usage / argument error.

## License

MIT. See `LICENSE` (or the license section below).

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
