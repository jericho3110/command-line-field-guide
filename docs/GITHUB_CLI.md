# GitHub CLI (`gh`) and the GitHub API

Git moves commits. Everything else on GitHub (creating repos, visibility,
security settings, CI runs, releases) was done with `gh`, GitHub's
command-line tool. Most calls were `gh api`, which sends one REST request.

## Contents

1. [Repositories](#1-repositories)
2. [Security settings through the API](#2-security-settings-through-the-api)
3. [CI and releases](#3-ci-and-releases)
4. [Logging in and permissions](#4-logging-in-and-permissions)
5. [References](#references)

---

## 1. Repositories

| Command | What it does |
| --- | --- |
| `gh repo create NAME --private --source . --remote origin --push` | create the GitHub repo from the current folder, add `origin`, push. **Private by default** |
| `gh repo create NAME --public …` | public: only after the checklist in [WORKFLOW.md](WORKFLOW.md#3-publishing-a-repo) |
| `gh repo view OWNER/NAME` | exit code 0 if it exists: "is the name free?" before creating |
| `gh repo view OWNER/NAME --json visibility --jq .visibility` | one field: `PUBLIC` or `PRIVATE` |
| `gh repo edit OWNER/NAME --visibility public --accept-visibility-change-consequences` | change visibility (the long flag is GitHub making you confirm) |
| `gh repo rename NEW -R OWNER/OLD --yes` | rename (GitHub redirects the old URL, until a new repo takes the old name) |
| `gh repo list OWNER --visibility public --json name,isFork` | audit what's public |

`--json` picks fields; `--jq` filters them with a [jq](https://jqlang.org/)
expression, so scripts get one clean value.

## 2. Security settings through the API

`gh api` sends a request to `https://api.github.com` with your login:

| Setting | Request |
| --- | --- |
| Dependabot alerts on | `gh api -X PUT repos/OWNER/NAME/vulnerability-alerts` |
| private vulnerability reporting on | `gh api -X PUT repos/OWNER/NAME/private-vulnerability-reporting` |
| secret scanning + push protection on | `gh api -X PATCH repos/OWNER/NAME -f 'security_and_analysis[secret_scanning][status]=enabled' -f 'security_and_analysis[secret_scanning_push_protection][status]=enabled'` |
| list open Dependabot alerts | `gh api 'repos/OWNER/NAME/dependabot/alerts?state=open'` |
| dismiss an alert that doesn't apply | `gh api -X PATCH repos/OWNER/NAME/dependabot/alerts/N -f state=dismissed -f dismissed_reason=not_used -f dismissed_comment='…'` |
| compare a fork with its parent | `gh api repos/OWNER/FORK/compare/PARENT_OWNER:main...OWNER:main --jq .ahead_by` |

| Flag | Meaning |
| --- | --- |
| `-X PUT` / `-X PATCH` | the HTTP method (GET is the default) |
| `-f key=value` | a string field in the request body |
| `--jq` | filter the JSON reply |

These four switches (Dependabot alerts, private vulnerability reporting,
secret scanning, push protection) were turned on for every public repo.

## 3. CI and releases

| Command | What it does |
| --- | --- |
| `gh run list -R OWNER/NAME --limit 3` | recent GitHub Actions runs and their result |
| `gh run watch RUN_ID --exit-status` | wait for a run; exit code says pass or fail |
| `gh workflow run FILE.yml -R OWNER/NAME` | start a workflow by hand (needs `workflow_dispatch:` in the file) |
| `gh api -X POST repos/OWNER/NAME/pages -f build_type=workflow` | turn on GitHub Pages deployed by a workflow |
| `gh release create v0.1.1 installer.exe SHA256SUMS --title … --notes-file …` | a release with files attached and a checksum file |

## 4. Logging in and permissions

```text
$ gh auth status
  ✓ Logged in to github.com account <you> (keyring)
  - Token scopes: 'gist', 'read:org', 'repo', 'workflow'
```

`gh` stores an OAuth token in the system's credential store. Its
**scopes** limit what it can do: deleting a repository needs `delete_repo`,
which isn't granted by default; `gh auth refresh -h github.com -s delete_repo`
asks for it in the browser, and `-r delete_repo` gives it back.

**Found live:** `gh repo delete` failed with `HTTP 403 … needs the
"delete_repo" scope`. That's least privilege working: a destructive power
must be granted on purpose.

## References

### Official

- GitHub CLI manual: [gh repo create](https://cli.github.com/manual/gh_repo_create), [gh repo edit](https://cli.github.com/manual/gh_repo_edit), [gh repo view](https://cli.github.com/manual/gh_repo_view), [gh api](https://cli.github.com/manual/gh_api), [gh run watch](https://cli.github.com/manual/gh_run_watch), [gh release create](https://cli.github.com/manual/gh_release_create), [gh auth refresh](https://cli.github.com/manual/gh_auth_refresh)
- GitHub REST API: [Repositories](https://docs.github.com/en/rest/repos/repos), [Dependabot alerts](https://docs.github.com/en/rest/dependabot/alerts), [Pages](https://docs.github.com/en/rest/pages/pages)
- GitHub Docs: [About secret scanning](https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning), [Privately reporting a vulnerability](https://docs.github.com/en/code-security/security-advisories/working-with-repository-security-advisories/configuring-private-vulnerability-reporting-for-a-repository)

### Further learning

- [jq tutorial](https://jqlang.org/tutorial/)
