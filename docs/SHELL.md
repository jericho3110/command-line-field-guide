# Shell commands: the ones actually used

About 690 shell calls in one session, in Git Bash (POSIX shell on
Windows) and Windows PowerShell. Counted by the first word of each
command; the numbers are approximate (lines inside scripts written with
`<<'EOF'` blocks get counted too, and were removed from this list).

## Contents

1. [The ranking](#1-the-ranking)
2. [Bash: the everyday set](#2-bash-the-everyday-set)
3. [Patterns that came up again and again](#3-patterns-that-came-up-again-and-again)
4. [PowerShell equivalents](#4-powershell-equivalents)
5. [Gotchas that bit](#5-gotchas-that-bit)
6. [References](#references)

---

## 1. The ranking

| # | Command | Times | What for |
| --- | --- | --- | --- |
| 1 | `cd` | ~460 | go to a project before running its tools |
| 2 | `grep` | ~330 | search text (see [REGEX.md](REGEX.md)) |
| 3 | `python` | ~325 | run tools, tests, small scripts |
| 4 | `git` | ~300 | see [COMMANDS.md](COMMANDS.md) |
| 5 | `head` / `tail` | ~230 / ~195 | first / last lines of long output |
| 6 | `echo` | ~225 | labels in output, small files |
| 7 | `cat` | ~125 | show a file, or write one with `<<'EOF'` |
| 8 | `gh` | ~120 | GitHub (see [GITHUB_CLI.md](GITHUB_CLI.md)) |
| 9 | `sed` | ~100 | edit text in place (`sed -i 's/old/new/'`) |
| 10 | `ls` | ~80 | list folders |
| 11 | `npm`, `cargo` | ~70, ~50 | build and test JavaScript/TypeScript and Rust projects |
| 12 | `rm`, `sort`, `find`, `curl`, `cut`, `wc` | 20–50 each | delete, sort, find files, fetch URLs, pick columns, count |
| | PowerShell: `Select-Object`, `Select-String`, `ForEach-Object`, `Where-Object`, `Get-ChildItem`, `Get-Content` | 35–240 each | the PowerShell versions of head/grep/loops/filters/ls/cat |

## 2. Bash: the everyday set

| Command | Example | Means |
| --- | --- | --- |
| `head -n N` / `tail -n N` | `npm test 2>&1 \| tail -5` | first / last N lines |
| `grep` | `grep -n -E 'error\|FAIL' log.txt` | lines matching a regex |
| `sed -i 's/a/b/' file` | change one line without opening an editor | in-place substitute |
| `cut -f1-3` / `cut -d, -f1` | columns from tab- / comma-separated text | pick columns |
| `wc -l` | `git ls-files \| wc -l` | count lines |
| `sort \| uniq -c \| sort -rn` | count duplicates, biggest first | frequency table |
| `find . -name '*.py' -not -path '*/.venv/*'` | files by name, skipping folders | file search |
| `curl -s -o /dev/null -w '%{http_code}' URL` | `200`, `404`… | is the link alive? |
| `cmd1 && cmd2` | `tests && git commit …` | run cmd2 **only if** cmd1 succeeded |
| `cmd1; cmd2` | | run both, whatever happens |
| `cmd 2>&1` | | send errors to the same place as output |
| `> file` / `>> file` | | write / append output to a file |
| `$(cmd)` | `echo "commits: $(git rev-list --all --count)"` | insert a command's output |
| `for d in */; do …; done` | run something in every project folder | loop |
| `cat > file <<'EOF' … EOF` | write a multi-line file (commit messages) | here-document; the quotes stop `$` expanding |

## 3. Patterns that came up again and again

```bash
# 1. Gate on the exit code, never on printed text
python main.py check && git commit -q -F msg.txt

# 2. Check many repos at once
for d in Teto_Desktop Disk_Cleanup Math/Unstoppable_Force; do
  echo "$d: $(git -C "$d" status --short | wc -l) uncommitted"
done

# 3. Is this web page the right one? (status code + title)
curl -s -L -A 'Mozilla/5.0' "$URL" | grep -o -i -E '<title>[^<]*' | head -1

# 4. Write a commit message without quoting trouble
cat > "$TEMP/m.txt" <<'EOF'
Add the thing

Why it was needed.
EOF
git commit -q -F "$TEMP/m.txt" && rm "$TEMP/m.txt"
```

## 4. PowerShell equivalents

| Bash | PowerShell |
| --- | --- |
| `head -5` / `tail -5` | `Select-Object -First 5` / `-Last 5` |
| `grep text` | `Select-String text` |
| `for x in …` | `foreach ($x in …) { }` or `… \| ForEach-Object { $_ }` |
| `ls` / `cat` | `Get-ChildItem` / `Get-Content` |
| `cmd1 && cmd2` | `cmd1; if ($?) { cmd2 }` (Windows PowerShell 5.1 has no `&&`) |
| `> file` | `Out-File -Encoding utf8` (adds a BOM in 5.1!) or `[IO.File]::WriteAllText(path, text, (New-Object Text.UTF8Encoding($false)))` |

## 5. Gotchas that bit

| Gotcha | What happened | Fix |
| --- | --- | --- |
| `tests \| grep OK && git commit` | commits even if tests fail: a pipeline's exit code is the **last** command's | `tests && git commit` |
| PowerShell 5.1 `Set-Content -Encoding utf8` | wrote a BOM into a commit message | `UTF8Encoding($false)` |
| a one-item PowerShell array | turned into a plain string and mangled a tool's arguments | build the argument list explicitly |
| `mv` on Windows: `Permission denied` | a program had a file open in the folder | close it, then move (see [MOVING_REPOS.md §6](MOVING_REPOS.md#6-found-live-reorganising-these-projects)) |
| `cmd /c start "" file` vs `start file` | Git Bash needs `cmd //c start "" file` | the `""` is the window title |
| a long-running browser screenshot never finished | headless Edge waited on infinite animations and the user's own profile | a separate `--user-data-dir` and a `timeout` |

## References

### Official

- [GNU Bash manual](https://www.gnu.org/software/bash/manual/bash.html) ([Pipelines](https://www.gnu.org/software/bash/manual/html_node/Pipelines.html), [Redirections](https://www.gnu.org/software/bash/manual/html_node/Redirections.html), [Here Documents](https://www.gnu.org/software/bash/manual/html_node/Redirections.html#Here-Documents))
- [GNU Coreutils manual](https://www.gnu.org/software/coreutils/manual/coreutils.html), [GNU sed](https://www.gnu.org/software/sed/manual/sed.html)
- Microsoft: [PowerShell 5.1 about_Pipelines](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_pipelines?view=powershell-5.1)

### Other

- [explainshell.com](https://explainshell.com/): paste a command, see each part explained

### Further learning

- [The Missing Semester (MIT): The Shell](https://missing.csail.mit.edu/2020/course-shell/), [Exercism Bash track](https://exercism.org/tracks/bash)
