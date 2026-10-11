# Moving a repository (and its history) somewhere else

"I want to put this repo inside another folder, but won't that mess things
up?" Usually not. Here's what moves with a repo, what doesn't, and the
one case that really does make a mess.

## Contents

1. [A repo is a folder with `.git` inside](#1-a-repo-is-a-folder-with-git-inside)
2. [What breaks when you move it (and the fixes)](#2-what-breaks-when-you-move-it-and-the-fixes)
3. [The real mess: a repo inside another repo](#3-the-real-mess-a-repo-inside-another-repo)
4. [Moving history between repositories](#4-moving-history-between-repositories)
5. [Moving files *within* a repo](#5-moving-files-within-a-repo)
6. [Found live: reorganising these projects](#6-found-live-reorganising-these-projects)
7. [Exercises](#7-exercises)
8. [References](#references)

---

## 1. A repo is a folder with `.git` inside

```text
Project_Phalanx/
  .git/          <- ALL history, branches, tags, and the remote URL (.git/config)
  src/  docs/    <- your files
```

Everything Git knows lives in `.git`, **inside** the folder. So moving the
folder (Explorer drag, `mv`, `Move-Item`) moves the whole repository,
history included. No Git command is needed, and GitHub doesn't care where
the folder sits on your disk. Check afterwards:

```bash
git -C NewParent/Project_Phalanx status          # still "nothing to commit"
git -C NewParent/Project_Phalanx log --oneline -1
git -C NewParent/Project_Phalanx remote -v       # same GitHub URL as before
```

## 2. What breaks when you move it (and the fixes)

Things *outside* Git that remember the **old absolute path**:

| Breaks | Why | Fix |
| --- | --- | --- |
| a Python **virtual environment** (`.venv`) | its launcher programs (`pip.exe`, console scripts) and an editable install's `.pth` file contain the old absolute path; Python's docs call venvs "inherently non-portable" | after moving: `.venv\Scripts\python -m pip install -e .`, or delete `.venv` and recreate it (`python -m venv .venv`, then reinstall) |
| scripts, docs or settings with hard-coded paths | they still point at the old place | search for the old path (`git grep -n 'Old_Folder'`) and update |
| editor workspaces, shortcuts, scheduled tasks | stored elsewhere | reopen the new folder |
| `node_modules`, Rust `target/`, build caches | usually fine (relative paths); if a tool complains, delete and rebuild | `npm ci`, `cargo build` |

**Before moving:** commit or stash your work (`git status` should be
clean), so a failed move can never lose anything.

## 3. The real mess: a repo inside another repo

If the **new parent is itself a Git repo**, the outer repo sees the inner
`.git` and records only a pointer (a *gitlink*), with this warning:

```text
warning: adding embedded git repository: Project_Phalanx
hint: You've added another git repository inside your current repository.
```

The outer repo's history then has no files from the inner one; clones of
the outer repo get an empty folder. Choose deliberately:

| Want | Do |
| --- | --- |
| independent projects side by side | make the parent a **plain folder**, not a repo (these side projects: `Side_Projects_For_Fun/` is not a repo, each project inside is) |
| the outer repo to *reference* the inner one at a fixed commit | `git submodule add https://github.com/OWNER/inner.git inner` |
| the inner project's **files and history merged into** the outer repo | `git subtree add --prefix=inner https://github.com/OWNER/inner.git main` |
| one repo, with the other's history moved into a subfolder | in a copy of the inner repo: `git filter-repo --to-subdirectory-filter inner`; then in the outer: `git remote add inner ../inner-copy`, `git fetch inner`, `git merge --allow-unrelated-histories inner/main` |

**Never `git init` a folder that contains other repos**, and never
`git init` inside an existing repo. Check first:
`git rev-parse --show-toplevel` (prints a path = you're already inside one).

## 4. Moving history between repositories

| Goal | Commands |
| --- | --- |
| same repo, new GitHub location | `git remote set-url origin https://github.com/OWNER/new.git` then `git push -u origin main` |
| rename on GitHub | `gh repo rename new-name` (GitHub redirects the old URL; update your remote with `set-url` to be tidy) |
| a full copy, every branch and tag | `git clone --mirror OLD_URL`, then `git push --mirror NEW_URL` |
| the current files **without** history (a fresh start) | `git archive HEAD \| tar -x -C ../fresh`, then `git init -b main` in `../fresh` |

The last one is what was used when an old repo's history contained a
personal email: the files moved, the history didn't (it was kept, private).

## 5. Moving files *within* a repo

```bash
git mv old/name.py new/place/name.py      # a move that Git records as one change
git log --follow -- new/place/name.py     # history from before the move too
```

Git doesn't store moves; it detects them by comparing content, so
`--follow` finds the old name. Moving a file with Explorer and then
`git add -A` gives the same result; `git mv` just does both steps.

## 6. Found live: reorganising these projects

The plan: move `Sacrament_Planner/` into `LDS_Church/` and
`Project_Phalanx/` into `Mabeys_Work/`, both plain folders. Both repos were
clean (`git status` empty), and Project-Phalanx's `.venv` was noted for
repair after the move.

What happened:

```text
$ mv Sacrament_Planner LDS_Church/
mv: cannot move 'Sacrament_Planner' to 'LDS_Church/Sacrament_Planner': Permission denied
```

**Why:** on Windows, a folder can't be renamed while a program holds a file
open inside it. The editor was watching the whole workspace (and OneDrive
syncs it). **What not to do:** copy, then delete the original. If the delete
fails halfway, you're left with two partial copies, which is how data gets
corrupted. **What to do:** close the editor (or pause OneDrive sync), move,
reopen, then check with `git status`.

## 7. Exercises

1. In a scratch folder, make a repo, commit, move the folder somewhere else, and run `git status` and `git log`. What changed?
2. Make repo `outer`, put repo `inner` inside it, run `git -C outer add -A`. Read the warning. Undo it with `git -C outer rm --cached inner`.
3. Rename a file with `git mv` and confirm `git log --follow` shows its old commits.

**Self-check:** why does moving a folder never need a Git command, but moving a Python venv does need a fix?

## References

### Official

- Pro Git: [Git Tools: Submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules); Git reference: [git-mv](https://git-scm.com/docs/git-mv), [git-remote](https://git-scm.com/docs/git-remote), [git-clone (--mirror)](https://git-scm.com/docs/git-clone), [git-subtree](https://github.com/git/git/blob/master/contrib/subtree/git-subtree.adoc), [git-log --follow](https://git-scm.com/docs/git-log)
- [git-filter-repo: --to-subdirectory-filter](https://github.com/newren/git-filter-repo/blob/main/Documentation/git-filter-repo.txt)
- Python: [venv: "inherently non-portable"](https://docs.python.org/3/library/venv.html)
- GitHub Docs: [Renaming a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository), [Transferring a repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/transferring-a-repository)

### Further learning

- Atlassian: [Git subtree vs submodule](https://www.atlassian.com/git/tutorials/git-subtree)
