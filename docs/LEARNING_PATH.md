# Learning path

Practise in a scratch repo in a folder **you** choose (never inside a real project).

| Stage | Read | Concepts | Exercise | Self-check |
| --- | --- | --- | --- | --- |
| 1 | [HOW_GIT_WORKS.md](HOW_GIT_WORKS.md) §1–3 | snapshots, hashes, the three areas, branches | its exercises 1–2 | what does the left column of `git status --short` mean? |
| 2 | [COMMANDS.md](COMMANDS.md) §1–2 | add, diff --staged, commit, push | make three commits with full messages (summary, why, how verified) | why read `git diff --staged` before committing? |
| 3 | COMMANDS §3–5 | log formats, pickaxe, show, archive | find when a line first appeared with `git log -S` | how would you list every author email in a repo? |
| 4 | [HOW_GIT_WORKS.md](HOW_GIT_WORKS.md) §5–7, [SECURITY.md](SECURITY.md) | permanent history, `.gitignore`, noreply identity | HOW_GIT_WORKS exercise 3 (the "deleted" secret) | why must a leaked key be revoked even after cleaning history? |
| 5 | [GITHUB_CLI.md](GITHUB_CLI.md), [WORKFLOW.md](WORKFLOW.md) | gh, API calls, publishing checklist | create a private repo with `gh repo create`, then delete it | why is `delete_repo` not granted by default? |
| 5b | [MOVING_REPOS.md](MOVING_REPOS.md) | moving repos, nested repos, submodule vs subtree, history transfer | its exercises 1–2 | why does moving a folder never need a Git command? |
| 5c | [REGEX.md](REGEX.md), [SHELL.md](SHELL.md) | regex building blocks, grep flags, pipes, exit codes | REGEX exercises; rewrite one Bash pattern in PowerShell | why is `tests \| grep OK && commit` dangerous? |
| 6 | COMMANDS §6, [FOUND_LIVE.md](FOUND_LIVE.md) | what not to do, and why | explain `--force` to a friend in two sentences | when would rewriting history ever be OK? |

## References

### Further learning

- [Learn Git Branching](https://learngitbranching.js.org/), [Oh My Git!](https://ohmygit.org/), [GitHub Skills](https://skills.github.com/)
