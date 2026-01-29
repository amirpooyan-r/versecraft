import 'package:flutter/material.dart';

import '../../core/utils/text_direction.dart';
import '../../i18n/l10n.dart';
import '../verse_picker/verse_picker_page.dart';
import '../verse_picker/verse_selection.dart';
import 'widgets/controls_panel.dart';
import 'widgets/verse_card.dart';

class EditorPage extends StatefulWidget {
  const EditorPage({super.key});

  @override
  State<EditorPage> createState() => _EditorPageState();
}

class _EditorPageState extends State<EditorPage> {
  VerseSelection? _selection;
  String _translationId = 'bsb';

  Future<void> _openVersePicker() async {
    final result = await Navigator.push<VerseSelection>(
      context,
      MaterialPageRoute(
        builder: (_) => VersePickerPage(
          translationId: _translationId,
          initialBookId: _selection?.bookId,
          initialChapter: _selection?.chapter,
        ),
      ),
    );

    if (!mounted || result == null) {
      return;
    }

    setState(() {
      _selection = result;
    });
  }

  @override
  Widget build(BuildContext context) {
    final strings = L10n.strings;
    final textDirection = AppTextDirection.forLocale(L10n.locale);
    final reference = _selection == null
        ? 'John 3:16'
        : _selection!.formatReference(dir: textDirection);

    return Scaffold(
      appBar: AppBar(title: Text(strings.appTitle)),
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            children: [
              Expanded(
                child: Center(
                  child: ConstrainedBox(
                    constraints: const BoxConstraints(maxWidth: 520),
                    child: AspectRatio(
                      aspectRatio: 1,
                      child: VerseCard(
                        textDirection: textDirection,
                        verseText: 'For God so loved the world...',
                        reference: reference,
                      ),
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 16),
              ControlsPanel(
                selectVerseLabel: strings.selectVerse,
                translationLabel: strings.translationLabel,
                layoutLabel: strings.layoutLabel,
                exportLabel: strings.exportLabel,
                onSelectVerse: _openVersePicker,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
