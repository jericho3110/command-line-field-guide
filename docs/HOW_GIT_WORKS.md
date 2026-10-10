# How Git works

The ideas you need so that every command in [COMMANDS.md](COMMANDS.md)
makes sense. Real output comes from this repository.

## Contents

1. [Snapshots, not diffs](#1-snapshots-not-diffs)
2. [The three areas: working tree, index, repository](#2-the-three-areas-working-tree-index-repository)
3. [Commits form a chain; branches are pointers](#3-commits-form-a-chain-branches-are-pointers)
4. [Remotes: your copy and GitHub's](#4-remotes-your-copy-and-githubs)
5. [History is permanent](#5-history-is-permanent)
6. [Files Git should ignore, and line endings](#6-files-git-should-ignore-and-line-endings)
7. [Who you are: author identity](#7-who-you-are-author-identity)
8. [Exercises](#8-exercises)
9. [References](#references)

---

## 1. Snapshots, not diffs

A commit is a **snapshot of every file**, not a list of changes. Git stores
it as small objects, each named by a **hash of its content** (SHA-1 by
default: 40 hex characters):

| Object | Holds | Example |
| --- | --- | --- |
| **blob** | one file's content (no name) | the text of `README.md` |
| **tree** | a folder: names → blobs and subtrees | `docs/` |
| **commit** | one tree + parent commit(s) + author + message | "Add a guide to Git…" |
| **tag** | a named pointer to a commit, optionally signed | `v0.1.0` |

`git cat-file -p HEAD` shows a commit object itself. Real output from this
repository's first commit (`637bf6d`):

```text
$ git cat-file -p 637bf6d
tree 140547b28aa14db5996a4e8635a58cb4e92ec929                                        <- the snapshot
author South Valley <93480907+jericho3110@users.noreply.github.com> 1791650093 +0800   <- noreply email; seconds since 1970 + timezone
committer South Valley <93480907+jericho3110@users.noreply.github.com> 1791650093 +0800

Add a guide to Git and the commands used most
```

The first commit has no `parent` line; every later one does. Following the
`tree` hash shows the snapshot: one line per file (a **blob**) or folder
(another **tree**):

```text
$ git cat-file -p 637bf6d^{tree}
100644 blob 3931a6063f6bc180218a462af0313812d7f591f6  .gitattributes
100644 blob eaba63869bbd18293559c87b50c31b8bafd024e3  README.md
040000 tree 749ee6e84de51044126d5ac1bdaaba6326fc9636  docs
100644 blob 3f3b0771ec878cefede0c09fc0908403fffdd1d3  main.py
…
```

`100644` is a normal file, `040000` a folder (git separates the name with a tab, shown here as spaces). Notice the tree has the
**names**; a blob is only content.

**Why hashes matter:** the same content always gets the same name
(*content addressing*). Change one byte anywhere and the hash of the file,
its folder, the commit, and every later commit changes. That's why history
can't be edited quietly, and why an unchanged file costs no extra space.

## 2. The three areas: working tree, index, repository

```text
  working tree            index (staging area)          repository (.git)
  your files on disk  ──git add──►  the next commit  ──git commit──►  permanent history
          ◄──────────── git restore ───────────┘                │
          ◄────────────────────── git checkout / switch ────────┘
```

- **Working tree:** the files you edit.
- **Index:** what the *next* commit will contain. `git add` copies a file's current content here.
- **Repository:** the `.git` folder, holding every snapshot ever committed.

The index lets you commit **some** changes and not others. That's how we
committed only our own files when someone else had uncommitted edits in
the same repo (`git add <named files>`, never "add everything").

## 3. Commits form a chain; branches are pointers

```text
a1b2c3 ◄── d4e5f6 ◄── 0c8f68e     ◄── main  ◄── HEAD
(first)               (newest)
```

- Each commit points to its **parent**: that's the history.
- A **branch** (`main`) is just a file containing one commit hash. Committing moves it forward.
- **HEAD** says which branch you're on.

These side projects use **one branch, `main`**, and commit straight to it.
That's fine when you're the only author; teams use feature branches and
pull requests so changes get reviewed before they reach `main`.

## 4. Remotes: your copy and GitHub's

Your repo and GitHub's are **two full copies**. A *remote* is a named URL
for the other copy; by convention `origin`.

| Command | Direction |
| --- | --- |
| `git push origin main` | your commits → GitHub |
| `git fetch` | GitHub's commits → your repo (doesn't touch your files) |
| `git pull` | fetch + merge into your branch |
| `git clone <url>` | a new full copy, with `origin` set up |

If GitHub has commits you don't, a push is **rejected**. The fix is to
fetch and merge, never `--force`, which would delete the other commits.

## 5. History is permanent

Anything committed stays in the history **even after you delete the file**:
deleting creates a *new* snapshot without it; the old snapshots still have
it. Pushed history is also copied to every clone and fork.

| What leaked | What doesn't fix it | What fixes it |
| --- | --- | --- |
| a secret (API key, password) | deleting the file | **revoke the secret** first; then clean or replace the history |
| personal data (an email in commits, names) | a new commit | a fresh repository from the current files (old one archived privately), or rewriting history and force-pushing, *with the owner's explicit OK* |

**Found live (case study):** two public repos showed a personal email
address as the author of every commit. The fix kept history safe instead
of rewriting it: the old repos were renamed `*-archive` and made private,
and new public repos were published from the latest files with the
GitHub *noreply* address. Details: [SECURITY.md](SECURITY.md).

## 6. Files Git should ignore, and line endings

**`.gitignore`** lists files Git should never add: build output, virtual
environments, `.env` secrets, logs, and **data folders with personal
information**. A data folder can also carry its own `.gitignore` containing
just `*`, which ignores everything inside it, so it's safe even if the
folder ends up inside a repo. `git check-ignore -v <file>` tells you which
rule matched.

**Line endings:** Windows uses CRLF (`\r\n`), Linux and macOS use LF
(`\n`). `.gitattributes` with `* text=auto` stores LF in the repository and
gives each platform its own on checkout. That's what this warning means:

```text
warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it
```

Harmless: Git is telling you it normalises line endings as configured.

## 7. Who you are: author identity

Every commit records an author name and email, from your config:

```bash
git config --global user.name  "Your Name"
git config --global user.email "<id>+<username>@users.noreply.github.com"
```

The **noreply** address (GitHub → Settings → Emails) keeps your real email
out of public history. Also tick **Block command line pushes that expose
my email**, so a misconfigured machine can't leak it.

## 8. Exercises

Make a practice repo in a folder you choose (not a project folder):

1. `git init -b main practice`, add a file, commit. Run `git cat-file -p HEAD`, then `git cat-file -p <the tree hash>`. What's in each?
2. Change two files, `git add` only one, run `git status --short`. What do the two columns mean?
3. Commit a file named `secret.txt`, delete it, commit again. Find it with `git log --all -- secret.txt` and `git show <hash>:secret.txt`. What does this teach you?
4. Add `*.log` to `.gitignore` and check it with `git check-ignore -v app.log`.

**Self-check:** why does editing one old commit change the hash of every commit after it?

## References

### Official

- Pro Git (free book): [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-What-is-Git%3F), [Git Objects](https://git-scm.com/book/en/v2/Git-Internals-Git-Objects), [Branches in a Nutshell](https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell), [Working with Remotes](https://git-scm.com/book/en/v2/Git-Basics-Working-with-Remotes)
- Git reference: [gitignore](https://git-scm.com/docs/gitignore), [gitattributes](https://git-scm.com/docs/gitattributes), [git-cat-file](https://git-scm.com/docs/git-cat-file), [git-config](https://git-scm.com/docs/git-config)
- GitHub Docs: [Setting your commit email address](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address), [Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

### Other

- Julia Evans, [How git works (zines and posts)](https://jvns.ca/categories/git/)
- [Think Like (a) Git](https://think-like-a-git.net/)

### Further learning

- [Learn Git Branching](https://learngitbranching.js.org/) (interactive, in the browser)
- [Oh My Git!](https://ohmygit.org/) (a game that teaches Git)
