# Security: keeping secrets and personal data out of Git

## Contents

1. [What can leak](#1-what-can-leak)
2. [Defenses, in order](#2-defenses-in-order)
3. [If something leaked](#3-if-something-leaked)
4. [Case studies (found live)](#4-case-studies-found-live)
5. [This repo](#5-this-repo)
6. [References](#references)

---

## 1. What can leak

| Leak | How it gets in | Who sees it |
| --- | --- | --- |
| secrets (API keys, tokens, passwords, `.env`) | committed by `git add -A`, pasted into a config | everyone, for a public repo; bots scan GitHub within minutes |
| **personal email** | the commit's *author* field, from `git config user.email` | everyone who views the history |
| personal data (names, phone numbers, addresses) | data files, test fixtures, examples, commit messages | everyone with access, forever |
| local paths and user names | logs, build output, docs pasted from a terminal | everyone |

The trap in all of these: **history is permanent** ([HOW_GIT_WORKS §5](HOW_GIT_WORKS.md#5-history-is-permanent)).

## 2. Defenses, in order

| Layer | Defense |
| --- | --- |
| before writing | keep data in a folder **outside** any repo, with its own `.gitignore` of `*` |
| before staging | `.gitignore`: `.env`, `*.csv` data, `venv/`, build output, logs |
| before committing | `git diff --staged`; a secret scanner on the staged files (gitleaks, or a project scan); tests use **made-up** names only |
| identity | commit with the GitHub **noreply** email; turn on "block command line pushes that expose my email" |
| on push | GitHub **push protection** rejects pushes containing known secret formats |
| before going public | scan the **whole history** ([WORKFLOW §3](WORKFLOW.md#3-publishing-a-repo)) |
| after | Dependabot alerts, secret scanning alerts, private vulnerability reporting |

## 3. If something leaked

1. **Secrets: revoke them first.** A pushed key must be treated as stolen, whatever you do to the history.
2. Then choose:

| Option | Good | Cost |
| --- | --- | --- |
| **fresh repo** from the current files, old repo renamed `*-archive` and made private | no force-push; nothing destroyed | old stars, issues and links don't carry over |
| **rewrite history** (`git filter-repo`) and force-push | same URL | rewrites every hash; every clone must re-clone; only with the owner's explicit OK |
| make the repo private | instant | copies already cloned or cached elsewhere aren't recalled |

## 4. Case studies (found live)

| Found | Fix |
| --- | --- |
| two public repos had a **personal email** as the author of every commit | fresh public repos from the latest files with the noreply address; old repos archived privately; the global `user.email` was already noreply, so no new leak |
| member data was moved into a folder next to several repos | a `.gitignore` of `*` *inside* the data folder, so it protects itself even if it ever ends up inside a repo |
| a guide's test data happened to use a **real** surname from a member list | swapped for made-up names; a sweep compares the repo against the real name list before each commit, without the list itself ever being committed |
| a history scan flagged a four-part library version number (like 4.10.x.y) as an "IP address" | a false positive; checked by hand, documented |

## 5. This repo

Docs only, plus a check gate: `python main.py check` runs a security scan
(secrets, personal data, dangerous code patterns) and a link check. It
contains no personal data: examples use `<you>`, `OWNER/NAME` and the
public GitHub handle only.

## References

### Official

- GitHub Docs: [Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository), [About push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection), [Blocking command line pushes that expose your personal email address](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/blocking-command-line-pushes-that-expose-your-personal-email-address)
- [git-filter-repo](https://github.com/newren/git-filter-repo), [gitleaks](https://github.com/gitleaks/gitleaks)

### Other

- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

### Further learning

- [GitHub Skills: Secure your repository's supply chain](https://github.com/skills/secure-repository-supply-chain)
