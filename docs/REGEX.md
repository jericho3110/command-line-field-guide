# Regular expressions: the ones actually used

A regular expression ("regex") describes a pattern of text. In this
session they ran inside about 330 `grep` calls, the editor's search
tool, and Python (`re.search`, `re.sub` and `re.finditer` most).

## Contents

1. [The building blocks used most](#1-the-building-blocks-used-most)
2. [Real patterns from this session](#2-real-patterns-from-this-session)
3. [grep flags used most](#3-grep-flags-used-most)
4. [Python's `re`](#4-pythons-re)
5. [Gotchas that bit](#5-gotchas-that-bit)
6. [Exercises](#6-exercises)
7. [References](#references)

---

## 1. The building blocks used most

| Piece | Means | Example |
| --- | --- | --- |
| `a\|b\|c` | **alternation**: any of these (by far the most used piece) | `gmail\|AppData\|password` |
| `^` / `$` | start / end of a line | `^#+ ` = a Markdown heading |
| `[a-z0-9._-]` | one character from a set | an email's local part |
| `[^<]*` | any characters **except** `<` | text up to the next tag |
| `\d` `\w` `\s` | digit, word character, whitespace | `\d{2}/\d{2}/\d{4}` |
| `{2,}` `{1,3}` `?` `*` `+` | how many times | `[0-9]{1,3}` |
| `\b` | word boundary | `\bgrep\b` won't match `egrep` |
| `( … )` | a group, to capture or to repeat | `([0-9]{1,3}\.){3}` |
| `(?i)` | case-insensitive | `(?i)private` |
| `\.` | a literal dot (a bare `.` means "any character") | `\.csv$` |
| `.*?` | as **few** as possible (lazy) | `<title>.*?</title>` |

## 2. Real patterns from this session

| Pattern | Finds | Used for |
| --- | --- | --- |
| `[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}` | email addresses | scanning repo histories for personal emails before going public |
| `\b([0-9]{1,3}\.){3}[0-9]{1,3}\b` | IPv4 addresses | finding real IPs in docs (it also matched a four-part version number: a false positive) |
| `gh[opsu]_[A-Za-z0-9]{20,}\|github_pat_[A-Za-z0-9_]{20,}\|AKIA[0-9A-Z]{16}\|-----BEGIN [A-Z ]*PRIVATE KEY` | GitHub tokens, AWS keys, private keys | a quick secret scan when the dedicated scanner was blocked |
| `<title>[^<]*` | a web page's title | checking a link opens the *right* page, not just any page |
| `^[A-Za-z0-9][A-Za-z0-9-]*\.[A-Za-z0-9][A-Za-z0-9-]*(@\d+(\.\d+){0,3})?$` | a VS Code extension id like `publisher.name@1.2.3` | an **allow-list** so no `&` or `\|` could reach a Windows batch file |
| `(\d{2})/(\d{2})/(\d{4})` | `dd/mm/yyyy` dates, as 3 groups | reading a planning sheet's dates |
| `^(elder\|sister\|brother)\s+` (case-insensitive) | a title before a name | matching "Sister Santos" with "Santos" |
| `,(\s*[\]}])` → `\1` | a trailing comma before `]` or `}` | cleaning JSON-with-comments before parsing |
| `<(\w+)\b[^>]*\bid="drill-L-0"[^>]*?(/?)>` | one SVG element by id, self-closing or not | inserting animations into an SVG sticker |
| `(?:^\|[\s;&\|(])git\s+([a-z][a-z-]+)` | `git <subcommand>` inside a long command | counting the commands in this guide |

## 3. grep flags used most

| Flag | Times | Means |
| --- | --- | --- |
| `-E` | ~137 | extended regex: `\|`, `+`, `?`, `{}` work without backslashes |
| `-n` | ~124 | show line numbers |
| `-i` | ~67 | ignore case |
| `-v` | ~35 | show lines that **don't** match (filter out noise) |
| `-o` | ~25 | print only the matching part |
| `-c` | ~19 | count matching lines |
| `-r` / `-l` | a few | search folders / list file names only |

## 4. Python's `re`

| Function | Used for |
| --- | --- |
| `re.search(p, s)` | is there a match anywhere? |
| `re.fullmatch(p, s)` | does the **whole** string match? (for validation, use this, not `match`) |
| `re.sub(p, repl, s)` | replace |
| `re.finditer(p, s)` | every match, with its groups |
| `re.split(p, s)` | split on a pattern (e.g. on `;`, `&&`, `\|`) |
| `re.compile(p)` | reuse one pattern many times |

Write patterns as **raw strings**: `r"\d{2}"`. In a normal string, `"\t"`
is a tab, not backslash-t.

## 5. Gotchas that bit

| Gotcha | What happened | Fix |
| --- | --- | --- |
| `.` matches anything | an IP pattern matched a library version number | check matches by hand; anchor and limit (`\b`, `{1,3}`) |
| `re.match` + `$` allows a trailing newline | `"a.b\n"` could slip through a validator | `re.fullmatch` |
| escapes in normal strings | `"\v"` became a vertical tab inside a Windows path | raw strings `r"..."` |
| a regex is not a parser | editing HTML/XML with regex is fragile | fine for one known file, with an XML parse afterwards as a self-check |
| greedy `.*` | `<.*>` eats from the first `<` to the **last** `>` | lazy `.*?`, or a negated class `[^>]*` |

## 6. Exercises

1. Write a regex for `YYYY-MM-DD` and test it with `re.fullmatch`.
2. Why does `\b([0-9]{1,3}\.){3}[0-9]{1,3}\b` accept `999.1.1.1`? Make it stricter.
3. Run `grep -rn -E 'TODO|FIXME' .` in a project, then add `| grep -v tests/` to hide one folder.

**Self-check:** when should you use `fullmatch` instead of `search`?

## References

### Official

- Python: [re](https://docs.python.org/3/library/re.html), [Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html)
- GNU grep: [manual](https://www.gnu.org/software/grep/manual/grep.html)

### Other

- [regular-expressions.info](https://www.regular-expressions.info/)

### Further learning

- [RegexOne (interactive lessons)](https://regexone.com/), [Regex Crossword](https://regexcrossword.com/)
