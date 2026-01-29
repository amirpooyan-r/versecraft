# VerseCraft
Create clean, shareable Bible verse images for social media.

## Overview
VerseCraft helps users turn Bible verses into beautiful images suitable for
sharing via messaging apps, RCS, and social networks (Instagram, Facebook,
etc.). It is not a Bible reader, not a study tool, and not a search engine.

VerseCraft is offline-first. There are no accounts, no analytics, no tracking,
and no APIs in v1.0.

## Why VerseCraft Exists
There are many Bible reading apps, but very few free, open-source tools focused
specifically on generating high-quality verse images for sharing. VerseCraft
aims for simplicity, beauty, and respect for Scripture.

## Supported languages & translations (v1.0)
UI languages:
- English
- Persian (Farsi)

Built-in Bible translations (Public Domain only):
- KJV (English)
- WEB (English)
- BSB (English)
- POV – Persian Old Version

Each translation is stored as a separate SQLite database file.

## Technical overview
- Flutter (Android-first; iOS/Web/Desktop planned)
- SQLite (one database per translation)
- Designed to run well on older Android devices

## Project status
- v1.0 — In development
- Current focus:
  - Verse image editor
  - Verse picker (Book / Chapter / Verse range)

## How to run
```bash
flutter pub get
flutter run
```

## A Note on Purpose
VerseCraft is offered freely as a gift to the Christian community. While
licensed under MIT, we encourage users and organizations to share improvements
back with the community whenever possible, in the spirit of service,
generosity, and stewardship.

> "Whatever you do, work at it with all your heart, as working for the Lord,
> not for human masters."
> — Colossians 3:23

## License
MIT License. All Bible texts included in v1.0 are Public Domain.
