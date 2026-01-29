import 'dart:io';

import 'package:flutter/services.dart';
import 'package:path/path.dart' as path;
import 'package:path_provider/path_provider.dart';

class SqliteAssetDb {
  const SqliteAssetDb();

  String assetPathFor(String translationId) {
    return 'assets/bibles/$translationId.sqlite';
  }

  Future<String> ensureDbPath(String translationId) async {
    final appDir = await getApplicationSupportDirectory();
    final targetDir = Directory(path.join(appDir.path, 'bibles'));
    if (!await targetDir.exists()) {
      await targetDir.create(recursive: true);
    }

    final dbPath = path.join(targetDir.path, '$translationId.sqlite');
    final dbFile = File(dbPath);
    if (await dbFile.exists()) {
      return dbPath;
    }

    final assetPath = assetPathFor(translationId);
    final byteData = await rootBundle.load(assetPath);
    final bytes = byteData.buffer.asUint8List(
      byteData.offsetInBytes,
      byteData.lengthInBytes,
    );
    await dbFile.writeAsBytes(bytes, flush: true);
    return dbPath;
  }
}
