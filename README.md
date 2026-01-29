# VerseCraft
Create clean, shareable Bible verse images.

## Overview
VerseCraft is an Android-first, offline-only app for turning Bible verses into
clean, shareable images. The goal is simple:
- Select a Bible verse
- Render it as a beautiful image
- Export and share on social media

There are no accounts, no analytics, no tracking, and no APIs in v1.0.
VerseCraft is not a Bible reader and not a search app.

## Supported translations (v1.0)
- KJV (English) — Public Domain
- WEB (English) — Public Domain
- BSB (English) — Public Domain (since 2023)
- POV (Persian Old Version) — Public Domain

Each translation is stored in its own SQLite database file.

## Technical stack
- Flutter (Android-first)
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

## Credits / License
MIT License. All Bible texts used are Public Domain.

## نسخه فارسی
ورس‌کرفت یک اپلیکیشن آفلاین است که برای ساخت تصویرهای تمیز و قابل‌اشتراک از آیات
کتاب مقدس طراحی شده است. هدف پروژه ساده است: انتخاب آیه، تولید تصویر زیبا، و
اشتراک‌گذاری در شبکه‌های اجتماعی.

در نسخه ۱٫۰ هیچ حساب کاربری، تحلیل‌گر رفتار، ردیابی یا API وجود ندارد. این برنامه
«کتاب‌خوان» نیست و قابلیت جست‌وجو هم ندارد. تمرکز روی تجربه‌ی ساخت تصویر آیه است.

تمام متون کتاب مقدس که در نسخه ۱٫۰ استفاده می‌شوند در حوزه عمومی هستند و با احترام
به کپی‌رایت انتخاب شده‌اند. هر ترجمه به صورت یک پایگاه داده SQLite جداگانه نگهداری
می‌شود.
