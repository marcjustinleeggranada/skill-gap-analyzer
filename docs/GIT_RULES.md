# Git rules

Every commit in this repository uses one identity.

- Name: Marc Justin Lee G. Granada
- Email: granadamarc96@gmail.com

No other name or email is correct. `granadam96@gmail.com` is wrong.

## Set up once per clone

Run inside the project folder. These commands change this clone only, never the global config.

```
git config user.name "Marc Justin Lee G. Granada"
git config user.email "granadamarc96@gmail.com"
git config core.hooksPath .githooks
```

The last line turns on the check in `.githooks/pre-push`. It refuses a push when any new commit has another author or committer email, or has a Co-Authored-By line, a "Generated with" line or a session trailer.

## Before every push

```
git pull origin main
git log -1 --format="%an <%ae> | %cn <%ce>"
```

The second command must print the name and email above on both sides of the bar. If it does not, fix the commit before pushing:

```
git commit --amend --reset-author --no-edit
```

## What went wrong on 2026-11-01

Two commits were pushed with `granadam96@gmail.com`: "Add sourced role profiles" and "Use sourced source column in role profiles". Each session started from a different saved email and none of them checked the author before pushing.

Rules that follow from it:

- Set the identity in the clone before the first commit of every session. Do not trust what a clone or a tool already has configured.
- Run the check above before every push, every time.
- Never push history rewrites on your own. Rewriting history needs a force push, and only the repository owner approves that.
- If a wrong commit is already pushed, tell the owner and stop. Do not stack more commits on top and do not rewrite anything.

## Fixing the two old commits (owner only)

The two commits are still in history. To correct them, the owner runs this from an up-to-date clone with no local changes, then force-pushes:

```
FILTER_BRANCH_SQUELCH_WARNING=1 git filter-branch -f --env-filter '
if [ "$GIT_AUTHOR_EMAIL" = "granadam96@gmail.com" ]; then export GIT_AUTHOR_EMAIL="granadamarc96@gmail.com"; fi
if [ "$GIT_COMMITTER_EMAIL" = "granadam96@gmail.com" ]; then export GIT_COMMITTER_EMAIL="granadamarc96@gmail.com"; fi
' -- main
git push --force-with-lease origin main
```

Everyone else then runs `git fetch origin` and `git reset --hard origin/main` in their clone. Any unpushed work in a clone is lost by that reset, so push or copy it first.

## Other rules

- Commit messages are short and factual: what changed and why.
- Run `git status` before every commit. Do not commit tool-generated folders, local config folders, `.env` files, keys or passwords.
- Keep every file in the repository tool-neutral.
