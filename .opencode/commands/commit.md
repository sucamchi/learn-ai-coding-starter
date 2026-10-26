---
description: Review the diff, stage and commit everything with a message, then rebase onto origin/main
---

Commit the current project changes under the message below, then sync with the
remote.

Commit message: $ARGUMENTS

## 1. Review the diff

Run `git status --short` and `git diff` — plus `git diff --staged` if anything is
already staged — and read the actual changes. This is a review, not a formality:
if the diff contains anything that should not be committed (secrets, `.env`
files, build output, accidentally deleted files, or changes unrelated to the
message), stop and report it instead of committing. The whole working tree is
being committed under one message, so the message has to describe all of it.

## 2. Stage and commit

```bash
git add -A
git commit -m "<the message above>"
```

Use the message exactly as given. If nothing was changed, say so and stop —
do not create an empty commit.

## 3. Rebase onto origin/main

```bash
git pull --rebase origin main
```

A rebase can conflict. If it does, stop and report the conflict rather than
resolving it by discarding either side, and do not force-push. Leave the
repository in a state the user can inspect, and tell them which files need
attention.

## 4. Report

Show the resulting commit (`git log --oneline -1` and `git show --stat`) and the
output of the rebase, so the user can confirm what was recorded and how the sync
went. Lead with any failure.
