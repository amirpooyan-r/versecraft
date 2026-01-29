import 'package:flutter/foundation.dart';
import 'package:sqflite/sqflite.dart';

import 'sqlite_asset_db.dart';

class SqliteVerseSource {
  SqliteVerseSource(this._assetDb);

  final SqliteAssetDb _assetDb;
  final Map<String, Database> _dbCache = {};
  final Map<String, bool> _schemaValidCache = {};

  Future<List<String>> getVerses({
    required String translationId,
    required String bookId,
    required int chapter,
    required int startVerse,
    required int endVerse,
  }) async {
    try {
      final db = await _openDb(translationId);
      final isValid = await _ensureSchemaValid(db, translationId);
      if (!isValid) {
        return [];
      }
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

  Future<bool> _ensureSchemaValid(Database db, String translationId) async {
    final cached = _schemaValidCache[translationId];
    if (cached != null) {
      return cached;
    }
    try {
      final hasVerses = await _tableExists(db, 'verses');
      if (!hasVerses) {
        _logSchemaIssue(
          translationId,
          'Missing required table "verses".',
        );
        _schemaValidCache[translationId] = false;
        return false;
      }

      final columns = await db.rawQuery('PRAGMA table_info(verses)');
      final columnNames = columns
          .map((row) => row['name'] as String?)
          .whereType<String>()
          .toSet();
      const requiredColumns = {'book', 'chapter', 'verse', 'text'};
      final missingColumns = requiredColumns
          .where((column) => !columnNames.contains(column))
          .toList();
      if (missingColumns.isNotEmpty) {
        _logSchemaIssue(
          translationId,
          'Missing required columns in "verses": ${missingColumns.join(', ')}.',
        );
        _schemaValidCache[translationId] = false;
        return false;
      }

      final hasMeta = await _tableExists(db, 'meta');
      if (!hasMeta) {
        _logSchemaIssue(
          translationId,
          'Optional table "meta" is missing.',
        );
      }

      _schemaValidCache[translationId] = true;
      return true;
    } catch (error) {
      _logSchemaIssue(
        translationId,
        'Schema validation failed: $error',
      );
      _schemaValidCache[translationId] = false;
      return false;
    }
  }

  Future<bool> _tableExists(Database db, String tableName) async {
    final rows = await db.rawQuery(
      'SELECT name FROM sqlite_master WHERE type = ? AND name = ?',
      ['table', tableName],
    );
    return rows.isNotEmpty;
  }

  void _logSchemaIssue(String translationId, String message) {
    debugPrint('SqliteVerseSource[$translationId]: $message');
  }
}
