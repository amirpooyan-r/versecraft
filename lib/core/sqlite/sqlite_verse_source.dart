import 'package:sqflite/sqflite.dart';

import 'sqlite_asset_db.dart';

class SqliteVerseSource {
  SqliteVerseSource(this._assetDb);

  final SqliteAssetDb _assetDb;
  final Map<String, Database> _dbCache = {};

  Future<List<String>> getVerses({
    required String translationId,
    required String bookId,
    required int chapter,
    required int startVerse,
    required int endVerse,
  }) async {
    try {
      final db = await _openDb(translationId);
      final rows = await db.query(
        'verses',
        columns: ['verse', 'text'],
        where: 'book = ? AND chapter = ? AND verse BETWEEN ? AND ?',
        whereArgs: [bookId, chapter, startVerse, endVerse],
        orderBy: 'verse',
      );
      return rows.map((row) => row['text'] as String).toList();
    } catch (_) {
      return [];
    }
  }

  Future<Database> _openDb(String translationId) async {
    final cached = _dbCache[translationId];
    if (cached != null && cached.isOpen) {
      return cached;
    }
    final path = await _assetDb.ensureDbPath(translationId);
    final db = await openDatabase(path, readOnly: true);
    _dbCache[translationId] = db;
    return db;
  }
}
