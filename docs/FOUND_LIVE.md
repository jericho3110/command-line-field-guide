# Found live: Git surprises on Windows

Real problems hit while working, with the cause and the fix.

| What happened | Why | Fix |
| --- | --- | --- |
| `warning: … LF will be replaced by CRLF` on every new file | `* text=auto` in `.gitattributes`: Git stores LF and checks out CRLF on Windows | nothing: it's a notice, not an error |
| a commit summary started with an invisible character | Windows PowerShell 5.1's `Set-Content -Encoding utf8` writes a **BOM** (`EF BB BF`) first | write message files as UTF-8 *without* BOM; a pushed commit can't be amended, so it stayed |
| `fatal: cannot write keep file … Filename too long` during `git clone` | Windows' 260-character path limit, hit by a deep temp folder | clone into a short path; or `git config --global core.longpaths true` |
| a tool said `nothing is staged` | no files were named and `--all` wasn't given | name the files, or pass `--all` on purpose |
| a Windows path written inside a small docs-editing script came out with a tab and a vertical tab in it | `\t` and `\v` inside a normal Python string are escape sequences | raw strings (`r"..."`), forward slashes, or an editor instead of a script |
| `git push` was fine but GitHub showed "1 vulnerability" | Dependabot scans the default branch after each push | read the alert; fix it, or dismiss it with a reason if it doesn't apply (here: a Linux-only library not built for Windows) |
| a pushed `go.mod` change fixed 9 vulnerabilities at once | the toolchain line (`toolchain go1.27.2`) made every build use the patched release | pin patched toolchains in the repo, so every machine gets the fix |
| GitHub Pages failed after a repo was recreated | the first push ran the deploy workflow before Pages was switched on | turn Pages on, then rerun the workflow (`gh workflow run`) |

## References

### Official

- [gitattributes: text=auto and eol](https://git-scm.com/docs/gitattributes#_end_of_line_conversion), [git-config: core.longpaths (Git for Windows)](https://github.com/git-for-windows/git/wiki/FAQ)
- Microsoft: [Set-Content -Encoding (PowerShell 5.1)](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/set-content?view=powershell-5.1), [Maximum path length limitation](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation)

### Further learning

- [Pro Git: Customizing Git, attributes](https://git-scm.com/book/en/v2/Customizing-Git-Git-Attributes)
