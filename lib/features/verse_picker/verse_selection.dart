import 'dart:ui';

class VerseSelection {
  const VerseSelection({
    required this.translationId,
    required this.bookId,
    required this.bookName,
    required this.chapter,
    required this.startVerse,
    required this.endVerse,
  });

  final String translationId;
  final String bookId;
  final String bookName;
  final int chapter;
  final int startVerse;
  final int endVerse;

  bool get isRange => startVerse != endVerse;

  String formatReference({required TextDirection dir}) {
    final verse = isRange ? '$startVerse–$endVerse' : '$startVerse';
    return '$bookName $chapter:$verse';
  }
}
