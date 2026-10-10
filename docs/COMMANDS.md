# The commands used most

Counted from one long working session (about 690 shell commands across
a dozen side projects), by searching the session log. The counts are
approximate: a pattern search also catches a few git commands written
inside scripts or commit messages.

## Contents

1. [The ranking](#1-the-ranking)
2. [Everyday commands](#2-everyday-commands)
3. [Looking at history](#3-looking-at-history)
4. [Inspecting a repo](#4-inspecting-a-repo)
5. [Setting up and copying](#5-setting-up-and-copying)
6. [Commands deliberately *not* used](#6-commands-deliberately-not-used)
7. [References](#references)

---

## 1. The ranking

| # | Command | Times | What for |
| --- | --- | --- | --- |
| 1 | `git log` | ~58 | history, authors, checking what was pushed |
| 2 | `git status` | ~52 | what changed, what's staged |
| 3 | `git add` | ~31 | choose what goes in the next commit |
| 4 | `git commit` | ~29 | save the snapshot |
| 5 | `git diff` | ~16 | review changes before committing |
| 6 | `git grep` | ~12 | search tracked files |
| 7 | `git init` | ~11 | new repositories |
| 8 | `git push` | ~11 | send commits to GitHub (often done by the gitship tool instead: ~26 more) |
| 9 | `git ls-files` | ~10 | which files are tracked |
| 10 | `git config` / `git show` | ~9 each | identity; one file from one commit |
| | `git rev-list`, `rev-parse`, `check-ignore`, `clone`, `fetch` | 3–8 each | counting, finding the repo, ignore rules, copies |

GitHub CLI (`gh`): about 70 calls in all, mostly `gh api` (security
settings), `gh repo view`, and `gh repo create`. See
[GITHUB_CLI.md](GITHUB_CLI.md).

## 2. Everyday commands

### `git status --short`

```text
 M README.md            <- modified, not staged (left column blank, right column M)
M  docs/COMMANDS.md     <- modified and staged (left column M)
A  docs/NEW.md          <- new file, staged
?? notes.txt            <- untracked: Git doesn't know it yet
```

Two columns: **left = index (staged)**, **right = working tree**. Run it
before and after every `add`, so you know exactly what the commit holds.

### `git add <files>`

| Form | Use |
| --- | --- |
| `git add README.md docs/` | **named files**: the default in these projects |
| `git add -A` | everything, including deletions: only after `git status` shows nothing unexpected |

Naming files is how we committed only our own work when another person
had uncommitted changes in the same repo.

### `git diff` and `git diff --staged`

| Form | Shows |
| --- | --- |
| `git diff` | working tree vs index: what you haven't staged |
| `git diff --staged` | index vs last commit: **exactly what the next commit will contain** |

Read the staged diff before every commit: it's the last chance to spot a
secret or a stray file.

### `git commit -q -F message.txt`

| Flag | Meaning |
| --- | --- |
| `-F <file>` | take the message from a file: long, multi-line messages without shell-quoting trouble |
| `-q` | quiet: print nothing on success |
| `-m "text"` | a short one-line message instead |

The message format used everywhere:

```text
Add tithing declaration scheduling          <- summary: imperative, ≤ 72 characters

Every household needs a declaration before   <- body: WHY, not what (the diff shows what)
year end; booking ~100 by hand is slow.

- tithing.py: one slot per household ...     <- related changes as bullets

Verified: python main.py check passes ...    <- how it was tested

Co-Authored-By: ...                          <- trailer
```

### `git push -q origin main`

Sends `main` to the remote `origin`. If it's **rejected** (GitHub has
commits you don't), `git fetch`, merge, then push again. **Never**
`--force` (§6).

## 3. Looking at history

| Command | Shows | Used for |
| --- | --- | --- |
| `git log --oneline -3` | `0c8f68e Add a sacrament…` one line each | "did my commit land?" |
| `git log --format='%h %an <%ae> %s'` | hash, author, **email**, summary | auditing author emails before going public |
| `git log -p --all` | every change in every commit on every branch | scanning the **whole history** for secrets and personal data |
| `git log -S'some text'` | commits that added or removed that text ("pickaxe") | finding when something entered the history |
| `git show HEAD:path/file` | one file as it was in a commit | reading old versions without checking them out |
| `git rev-list --all --count` | number of commits | quick size of a repo's history |

Format placeholders: `%h` short hash, `%an` author name, `%ae` author
email, `%s` subject, `%ad` date (with `--date=short`).

## 4. Inspecting a repo

| Command | Shows | Used for |
| --- | --- | --- |
| `git rev-parse --show-toplevel` | the repo's root folder, or an error | "am I inside a repo?" before `git init` (never nest repos) |
| `git ls-files` | every tracked file | proving no data file is tracked: `git ls-files \| grep '\.csv$'` |
| `git check-ignore -v file` | which `.gitignore` rule ignores a file | checking a data folder is protected |
| `git grep -n 'text'` | matches in tracked files only | searching without hitting build output |
| `git remote -v` | remote names and URLs | "is this repo on GitHub yet?" |
| `git config --global user.email` | the commit email | checking it's the noreply address |
| `git -C <dir> <command>` | run in another folder | scripts that check many repos |

## 5. Setting up and copying

| Command | Meaning |
| --- | --- |
| `git init -b main` | new repo whose first branch is `main` |
| `git clone <url> <dir>` | full copy of a remote repo |
| `git clone --no-checkout <url>` | history only, no files on disk: enough for scanning history |
| `git fetch --all` | download every remote branch |
| `git archive HEAD \| tar -x -C out/` | the **current files without any history**: how a fresh repo was made from an old one whose history contained a personal email |

## 6. Commands deliberately *not* used

| Command | Why not |
| --- | --- |
| `git push --force` | overwrites GitHub's history: deletes other people's commits and breaks every clone |
| `git commit --amend` on a pushed commit | changes a published commit's hash: the same problem as force-pushing |
| `git reset --hard` | throws away uncommitted work with no undo |
| `git rebase -i` | interactive: needs an editor, and rewriting history is rarely needed in a one-person project |
| `git filter-repo` / BFG (rewrite history) | only with the owner's explicit OK; a fresh repo is often simpler and keeps the old history archived |
| `git add .` without looking | sweeps up secrets, data files and other people's changes |
| skipping hooks (`--no-verify`) | hooks are checks; skipping them hides problems |

**Found live:** a commit summary once started with an invisible `BOM`
character, because the message file was written with Windows
PowerShell's `Set-Content -Encoding utf8`, which adds one. A pushed commit
can't be amended (above), so it stayed. Message files are now written as
UTF-8 *without* a BOM. More in [FOUND_LIVE.md](FOUND_LIVE.md).

## References

### Official

- Git reference: [git-status](https://git-scm.com/docs/git-status), [git-add](https://git-scm.com/docs/git-add), [git-diff](https://git-scm.com/docs/git-diff), [git-commit](https://git-scm.com/docs/git-commit), [git-push](https://git-scm.com/docs/git-push), [git-log](https://git-scm.com/docs/git-log) (incl. pretty formats), [git-show](https://git-scm.com/docs/git-show), [git-rev-list](https://git-scm.com/docs/git-rev-list), [git-rev-parse](https://git-scm.com/docs/git-rev-parse), [git-ls-files](https://git-scm.com/docs/git-ls-files), [git-check-ignore](https://git-scm.com/docs/git-check-ignore), [git-grep](https://git-scm.com/docs/git-grep), [git-clone](https://git-scm.com/docs/git-clone), [git-archive](https://git-scm.com/docs/git-archive), [git-init](https://git-scm.com/docs/git-init)
- Pro Git: [Recording changes](https://git-scm.com/book/en/v2/Git-Basics-Recording-Changes-to-the-Repository), [Viewing the commit history](https://git-scm.com/book/en/v2/Git-Basics-Viewing-the-Commit-History)

### Other

- Chris Beams, [How to Write a Git Commit Message](https://cbea.ms/git-commit/)
- [Conventional Commits](https://www.conventionalcommits.org/) (a different message style these projects chose not to use)

### Further learning

- [Git cheat sheet (GitHub Education)](https://education.github.com/git-cheat-sheet-education.pdf)
- [Exercism: Git-focused workflow](https://exercism.org/docs/using/solving-exercises/working-locally)
