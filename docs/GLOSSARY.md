# Glossary

| Term | Meaning | Explained in |
| --- | --- | --- |
| repository (repo) | a project folder plus its full history (`.git`) | [HOW §1](HOW_GIT_WORKS.md#1-snapshots-not-diffs) |
| commit | one snapshot of every file, with author, message and parent | [HOW §1](HOW_GIT_WORKS.md#1-snapshots-not-diffs) |
| hash (SHA) | the content-based name of an object, e.g. `0c8f68e` | [HOW §1](HOW_GIT_WORKS.md#1-snapshots-not-diffs) |
| blob / tree | a file's content / a folder listing, inside `.git` | [HOW §1](HOW_GIT_WORKS.md#1-snapshots-not-diffs) |
| working tree | your files on disk | [HOW §2](HOW_GIT_WORKS.md#2-the-three-areas-working-tree-index-repository) |
| index (staging area) | what the next commit will contain | [HOW §2](HOW_GIT_WORKS.md#2-the-three-areas-working-tree-index-repository) |
| branch | a movable pointer to a commit | [HOW §3](HOW_GIT_WORKS.md#3-commits-form-a-chain-branches-are-pointers) |
| HEAD | the branch (or commit) you're on | [HOW §3](HOW_GIT_WORKS.md#3-commits-form-a-chain-branches-are-pointers) |
| remote / origin | another copy of the repo, usually on GitHub / its default name | [HOW §4](HOW_GIT_WORKS.md#4-remotes-your-copy-and-githubs) |
| push / fetch / pull | send commits / download commits / download and merge | [HOW §4](HOW_GIT_WORKS.md#4-remotes-your-copy-and-githubs) |
| force-push | overwrite the remote's history (avoid) | [COMMANDS §6](COMMANDS.md#6-commands-deliberately-not-used) |
| pickaxe | `git log -S`: find commits that added or removed some text | [COMMANDS §3](COMMANDS.md#3-looking-at-history) |
| `.gitignore` / `.gitattributes` | files Git ignores / per-file settings like line endings | [HOW §6](HOW_GIT_WORKS.md#6-files-git-should-ignore-and-line-endings) |
| CRLF / LF | Windows / Unix line endings | [HOW §6](HOW_GIT_WORKS.md#6-files-git-should-ignore-and-line-endings) |
| noreply email | GitHub's private commit address | [HOW §7](HOW_GIT_WORKS.md#7-who-you-are-author-identity) |
| push protection | GitHub refuses pushes containing known secret formats | [SECURITY §2](SECURITY.md#2-defenses-in-order) |
| scope (token) | a permission a login token has, e.g. `repo`, `delete_repo` | [GITHUB_CLI §4](GITHUB_CLI.md#4-logging-in-and-permissions) |
| submodule / subtree | a repo inside a repo by reference / by copying its files and history in | [MOVING §3](MOVING_REPOS.md#3-the-real-mess-a-repo-inside-another-repo) |
| regex | a pattern describing text | [REGEX](REGEX.md) |
| pipeline / exit code | `a \| b` chains commands; the exit code says success (0) or failure | [SHELL](SHELL.md) |
| BOM | an invisible marker some editors put at the start of a UTF-8 file | [FOUND_LIVE](FOUND_LIVE.md) |

## References

### Official

- [Git glossary](https://git-scm.com/docs/gitglossary), [GitHub glossary](https://docs.github.com/en/get-started/learning-about-github/github-glossary)
