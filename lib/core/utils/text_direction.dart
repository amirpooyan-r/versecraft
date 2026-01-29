import 'package:flutter/widgets.dart';

class AppTextDirection {
  static TextDirection fromString(String value) {
    return value.toLowerCase() == 'rtl' ? TextDirection.rtl : TextDirection.ltr;
  }

  static TextDirection forLocale(Locale locale) {
    return locale.languageCode.toLowerCase() == 'fa'
        ? TextDirection.rtl
        : TextDirection.ltr;
  }
}
