# 0003 - Storage: SQLite Per Translation

## Status
Accepted

## Context
Translations are offline and need a simple storage strategy.

## Decision
Each translation is stored in its own SQLite database file. Even though the
database files are not yet added, the assets registry points to one `.sqlite`
file per translation.

## Consequences
Translation loading remains isolated and predictable, and upgrades can be
handled per translation file.
