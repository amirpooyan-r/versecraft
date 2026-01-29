import 'package:flutter/material.dart';

import '../../i18n/l10n.dart';
import 'mock_bible.dart';
import 'verse_selection.dart';

class VersePickerPage extends StatefulWidget {
  const VersePickerPage({
    super.key,
    required this.translationId,
    this.initialBookId,
    this.initialChapter,
  });

  final String translationId;
  final String? initialBookId;
  final int? initialChapter;

  @override
  State<VersePickerPage> createState() => _VersePickerPageState();
}

class _VersePickerPageState extends State<VersePickerPage> {
  late MockBook _selectedBook;
  late int _selectedChapter;
  int? _startVerse;
  int? _endVerse;

  @override
  void initState() {
    super.initState();
    _selectedBook = findMockBook(widget.initialBookId ?? '') ?? mockBooks.first;
    _selectedChapter = widget.initialChapter ?? 1;
  }

  void _onVerseTap(int verse) {
    setState(() {
      if (_startVerse == null) {
        _startVerse = verse;
        _endVerse = verse;
        return;
      }

      final hasRange = _endVerse != null && _endVerse != _startVerse;
      if (hasRange) {
        _startVerse = verse;
        _endVerse = verse;
        return;
      }

      if (verse == _startVerse) {
        _endVerse = verse;
        return;
      }

      final start = _startVerse!;
      _startVerse = verse < start ? verse : start;
      _endVerse = verse < start ? start : verse;
    });
  }

  void _onDone() {
    final start = _startVerse;
    if (start == null) {
      return;
    }
    final end = _endVerse ?? start;
    Navigator.pop(
      context,
      VerseSelection(
        translationId: widget.translationId,
        bookId: _selectedBook.id,
        bookName: _selectedBook.name,
        chapter: _selectedChapter,
        startVerse: start,
        endVerse: end,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final strings = L10n.strings;
    final chapters = mockChapters();
    final verses = mockVerses();

    return Scaffold(
      appBar: AppBar(title: Text(strings.selectVerse)),
      body: SafeArea(
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
              child: Row(
                children: [
                  Expanded(
                    child: DropdownButtonFormField<MockBook>(
                      initialValue: _selectedBook,
                      decoration: InputDecoration(
                        labelText: strings.book,
                        border: const OutlineInputBorder(),
                      ),
                      items: [
                        for (final book in mockBooks)
                          DropdownMenuItem(value: book, child: Text(book.name)),
                      ],
                      onChanged: (value) {
                        if (value == null) {
                          return;
                        }
                        setState(() {
                          _selectedBook = value;
                          _startVerse = null;
                          _endVerse = null;
                        });
                      },
                    ),
                  ),
                  const SizedBox(width: 12),
                  SizedBox(
                    width: 120,
                    child: DropdownButtonFormField<int>(
                      initialValue: _selectedChapter,
                      decoration: InputDecoration(
                        labelText: strings.chapter,
                        border: const OutlineInputBorder(),
                      ),
                      items: [
                        for (final chapter in chapters)
                          DropdownMenuItem(
                            value: chapter,
                            child: Text('$chapter'),
                          ),
                      ],
                      onChanged: (value) {
                        if (value == null) {
                          return;
                        }
                        setState(() {
                          _selectedChapter = value;
                          _startVerse = null;
                          _endVerse = null;
                        });
                      },
                    ),
                  ),
                ],
              ),
            ),
            Expanded(
              child: GridView.builder(
                padding: const EdgeInsets.all(16),
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 5,
                  crossAxisSpacing: 12,
                  mainAxisSpacing: 12,
                  childAspectRatio: 1.3,
                ),
                itemCount: verses.length,
                itemBuilder: (context, index) {
                  final verse = verses[index];
                  final isSelected =
                      _startVerse != null &&
                      _endVerse != null &&
                      verse >= _startVerse! &&
                      verse <= _endVerse!;
                  return OutlinedButton(
                    onPressed: () => _onVerseTap(verse),
                    style: OutlinedButton.styleFrom(
                      backgroundColor: isSelected
                          ? Theme.of(context).colorScheme.primaryContainer
                          : null,
                    ),
                    child: Text('$verse'),
                  );
                },
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: BottomAppBar(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: Row(
            children: [
              TextButton(
                onPressed: () => Navigator.pop(context),
                child: Text(strings.cancel),
              ),
              const Spacer(),
              FilledButton(
                onPressed: _startVerse == null ? null : _onDone,
                child: Text(strings.done),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
