import 'package:flutter/material.dart';

import 'strings_en.dart';
import 'strings_fa.dart';

abstract class VerseStrings {
  String get appTitle;
  String get selectVerse;
  String get done;
  String get cancel;
  String get book;
  String get chapter;
  String get translationLabel;
  String get layoutLabel;
  String get exportLabel;
}

class L10n {
  static Locale _locale = const Locale('en');

  static Locale get locale => _locale;

  static void setLocale(Locale locale) {
    _locale = locale;
  }

  static VerseStrings get strings {
    // TODO: Replace with Flutter localization + ARB files.
    switch (_locale.languageCode) {
      case 'fa':
        return StringsFa();
      default:
        return StringsEn();
    }
  }
}
