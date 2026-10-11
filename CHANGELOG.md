# Changelog

Format: [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions: [SemVer](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- MOVING_REPOS §6: how the reorganisation ended (script, all moves clean) and the in-place venv repair.

## [0.2.0] - 2026-10-11

### Added
- `docs/MOVING_REPOS.md`: moving a repo into another folder safely, nested repos (submodule, subtree, merging histories), moving history between repos, `git mv`, and the found-live Windows folder lock.
- `docs/REGEX.md` and `docs/SHELL.md`: the regular expressions and shell commands used most, counted from the session log, with gotchas.

### Changed
- Renamed from "Git Guide" to **Command-Line Field Guide** (repo `command-line-field-guide`): it now covers regex and the shell too.

## [0.1.0] - 2026-10-11

### Added
- How Git works (snapshots and hashes, the three areas, branches, remotes, permanent history, ignore rules, line endings, identity).
- The most-used commands, ranked from a real session's log, with flags, examples and the commands deliberately not used.
- GitHub CLI and API (repos, visibility, security settings, CI, releases, scopes), the commit and publishing workflow, security (leaks, defenses, recovery, case studies), Windows surprises, learning path, glossary.
- `python main.py check`: security scan and link check.
