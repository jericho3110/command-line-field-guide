# Command-Line Field Guide

Git, GitHub, regular expressions and the shell, explained through the
commands that were actually used most while building a dozen side
projects (measured from a real working session's log), with the safety
habits that keep secrets and personal data out of history.

## Contents

- [Start here](#start-here)
- [The top 10 at a glance](#the-top-10-at-a-glance)
- [Checks](#checks)
- [References](#references)

## Start here

| Doc | What's in it |
| --- | --- |
| [docs/HOW_GIT_WORKS.md](docs/HOW_GIT_WORKS.md) | **the ideas**: snapshots and hashes, working tree / index / repository, branches as pointers, remotes, why history is permanent, `.gitignore`, line endings, author identity |
| [docs/COMMANDS.md](docs/COMMANDS.md) | **the commands used most**, ranked by real usage, with every flag explained, plus the ones deliberately *not* used |
| [docs/GITHUB_CLI.md](docs/GITHUB_CLI.md) | `gh`: creating repos, visibility, security settings through the API, CI runs, releases, login scopes |
| [docs/MOVING_REPOS.md](docs/MOVING_REPOS.md) | moving a repo into another folder: what moves with it, what breaks (venvs, paths), the real mess (a repo inside a repo: submodule / subtree / merge), moving history between repos, `git mv` |
| [docs/REGEX.md](docs/REGEX.md) | the regular expressions used most: building blocks, real patterns (emails, IPs, secrets, allow-lists), grep flags, Python `re`, gotchas |
| [docs/SHELL.md](docs/SHELL.md) | the shell commands used most (Bash and PowerShell), recurring patterns, gotchas |
| [docs/WORKFLOW.md](docs/WORKFLOW.md) | the commit routine, publishing a repo safely, and automating both |
| [docs/SECURITY.md](docs/SECURITY.md) | what can leak, layered defenses, what to do after a leak, real case studies |
| [docs/FOUND_LIVE.md](docs/FOUND_LIVE.md) | Git surprises on Windows, with causes and fixes |
| [docs/LEARNING_PATH.md](docs/LEARNING_PATH.md), [docs/GLOSSARY.md](docs/GLOSSARY.md) | reading order with exercises; terms |
| [CHANGELOG.md](CHANGELOG.md) | versions |

## The top 10 at a glance

```bash
git status --short                 # what changed; left column = staged
git add README.md docs/            # stage named files, not everything
git diff --staged                  # exactly what the next commit holds
git commit -q -F message.txt       # commit with a message from a file
git push -q origin main            # send to GitHub (never --force)
git log --oneline -3               # did it land?
git log --format='%h %an <%ae> %s' # who committed, with which email
git grep -n 'text'                 # search tracked files
git ls-files                       # what is tracked
git rev-parse --show-toplevel      # am I inside a repo?
```

## Checks

`python main.py check` runs a security scan (secrets, personal data,
dangerous patterns) and a link check over the docs.

## References

### Official

- [Pro Git (free book)](https://git-scm.com/book/en/v2), [Git reference](https://git-scm.com/docs), [GitHub CLI manual](https://cli.github.com/manual/)

### Further learning

- [Learn Git Branching](https://learngitbranching.js.org/)

## License

[MIT](LICENSE)
