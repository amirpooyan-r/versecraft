import 'package:flutter/material.dart';

import '../features/editor/editor_page.dart';
import '../features/verse_picker/verse_picker_page.dart';

class AppRoutes {
  static const String editor = '/';
  static const String versePicker = '/verse-picker';

  static Map<String, WidgetBuilder> get routes => {
    editor: (_) => const EditorPage(),
    versePicker: (_) => const VersePickerPage(translationId: 'bsb'),
  };
}
