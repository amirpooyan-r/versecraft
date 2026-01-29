import 'package:flutter/material.dart';

import '../../core/sqlite/sqlite_asset_db.dart';
import '../../core/sqlite/sqlite_verse_source.dart';
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
  final String _translationId = 'bsb';
  final SqliteVerseSource _verseSource = SqliteVerseSource(
    const SqliteAssetDb(),
  );
  String? _verseText;
  bool _isLoading = false;

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

    await _loadVerses(result);
  }

  Future<void> _loadVerses(VerseSelection selection) async {
    setState(() {
      _isLoading = true;
    });

    final verses = await _verseSource.getVerses(
      translationId: selection.translationId,
      bookId: selection.bookId,
      chapter: selection.chapter,
      startVerse: selection.startVerse,
      endVerse: selection.endVerse,
    );

    if (!mounted) {
      return;
    }

    setState(() {
      _verseText = verses.isEmpty
          ? 'Verse text not available yet (SQLite DB not installed).'
          : verses.join(' ');
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    final strings = L10n.strings;
    final textDirection = AppTextDirection.forLocale(L10n.locale);
    final reference = _selection == null
        ? 'John 3:16'
        : _selection!.formatReference(dir: textDirection);
    final verseText = _selection == null
        ? 'For God so loved the world...'
        : _verseText;

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
                        verseText:
                            verseText ??
                            'Verse text not available yet (SQLite DB not installed).',
                        reference: reference,
                      ),
                    ),
                  ),
                ),
              ),
              const SizedBox(height: 16),
              if (_isLoading) ...[
                const SizedBox(height: 8),
                const SizedBox(
                  height: 24,
                  width: 24,
                  child: CircularProgressIndicator(strokeWidth: 2),
                ),
                const SizedBox(height: 8),
              ],
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
