import 'package:flutter/material.dart';

import '../../i18n/l10n.dart';

class VersePickerPage extends StatelessWidget {
  const VersePickerPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(L10n.strings.selectVerse)),
      body: const Center(child: Text('Verse selection will live here.')),
    );
  }
}
