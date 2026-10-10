# The workflow: from change to GitHub

How every commit in these projects was made, and how a repo goes public.

## Contents

1. [Which repository?](#1-which-repository)
2. [The commit routine](#2-the-commit-routine)
3. [Publishing a repo](#3-publishing-a-repo)
4. [Automating it: a small "ship" tool](#4-automating-it-a-small-ship-tool)
5. [References](#references)

---

## 1. Which repository?

Before the first commit in a folder:

```text
git rev-parse --show-toplevel        inside a repo?  -> use it, never create a repo inside it
search below for .git folders        found some?     -> this is a parent folder: never `git init` it;
                                                        each project folder gets its own repo
nothing anywhere                     -> `git init -b main` the project folder
```

**Never nest repositories.** A parent folder full of projects
(`Side_Projects_For_Fun/`) is *not* a repo; each project inside is.
Personal data lives in its own folder beside the repos, never inside one.

## 2. The commit routine

```text
1. run the project's checks (tests, linter, security scan, link check)   -> only continue if they pass
2. git status --short                                                    -> know what changed
3. git add <named files>                                                 -> only your own changes
4. git diff --staged   +   a secret scan (gitleaks / devtools)           -> nothing sensitive staged
5. git commit -q -F message.txt                                          -> why, related changes, how verified
6. git push -q origin main                                               -> never --force
7. git log --oneline -1                                                  -> report hash + summary
```

**Gate on exit codes, not on printed text.** `tests && git commit …`
commits only if the tests *succeed*. `tests | grep OK && git commit …`
commits whenever *grep* finds "OK", even if the tests failed, because a
pipeline's exit code is the last command's.

## 3. Publishing a repo

Private first. Public only after this checklist:

| Step | How |
| --- | --- |
| scan **the whole history**, not just the files | `gitleaks git .` for secrets; `git log --format='%an <%ae>'` for author emails; `git log -p --all` searched for names, local paths, IP addresses |
| history not clean? | publish a **fresh** repo from the current files (`git archive`), keep the old one private as an archive; or rewrite only with the owner's OK |
| a license | `LICENSE` (MIT in these projects) |
| make it public | `gh repo edit … --visibility public --accept-visibility-change-consequences` |
| turn on protections | Dependabot alerts, private vulnerability reporting, secret scanning, push protection ([GITHUB_CLI.md §2](GITHUB_CLI.md#2-security-settings-through-the-api)) |
| check it as a stranger | `curl -s -o /dev/null -w '%{http_code}' https://github.com/OWNER/NAME` → `200` |

## 4. Automating it: a small "ship" tool

Doing §2 by hand 30 times invites mistakes, so it was wrapped in a small
command-line tool (`gitship`, in another project) that:

| Step | Safety rule it enforces |
| --- | --- |
| runs the repo's configured checks first | no commit if a check fails |
| stages only the files you name (or `--all` when asked) | no sweeping up other changes |
| scans the staged files for secrets and personal data | stops before the commit, not after |
| rejects messages with `feat:`-style prefixes or a lowercase start | one message style everywhere |
| pushes, never with `--force` | history is never overwritten |

**Found live:** the tool rejected *its author's own* message
`docs: natural-mouse is public now` ("Conventional Commits prefix"),
which is exactly what a guard rail is for.

## References

### Official

- Pro Git: [Git Basics](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository), [Distributed workflows](https://git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows)
- [gitleaks](https://github.com/gitleaks/gitleaks)
- Bash manual: [Pipelines (exit status)](https://www.gnu.org/software/bash/manual/html_node/Pipelines.html)

### Further learning

- [GitHub flow](https://docs.github.com/en/get-started/using-github/github-flow) (the branch + pull-request workflow teams use)
