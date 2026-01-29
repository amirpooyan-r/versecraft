import 'dart:convert';

import 'package:flutter/services.dart';

import 'constants.dart';
import 'utils/text_direction.dart';

class TranslationInfo {
  const TranslationInfo({
    required this.id,
    required this.name,
    required this.lang,
    required this.direction,
    required this.assetDb,
    required this.publicDomain,
  });

  final String id;
  final String name;
  final String lang;
  final TextDirection direction;
  final String assetDb;
  final bool publicDomain;

  factory TranslationInfo.fromJson(Map<String, dynamic> json) {
    return TranslationInfo(
      id: json['id'] as String,
      name: json['name'] as String,
      lang: json['lang'] as String,
      direction: AppTextDirection.fromString(json['direction'] as String),
      assetDb: json['assetDb'] as String,
      publicDomain: json['publicDomain'] as bool? ?? false,
    );
  }
}

class TranslationRegistry {
  const TranslationRegistry({
    required this.defaultTranslationId,
    required this.items,
  });

  final String defaultTranslationId;
  final List<TranslationInfo> items;

  static Future<TranslationRegistry> load() async {
    try {
      final raw = await rootBundle.loadString(
        AppConstants.translationsAssetPath,
      );
      final data = jsonDecode(raw) as Map<String, dynamic>;
      final items = (data['items'] as List<dynamic>)
          .map((item) => TranslationInfo.fromJson(item as Map<String, dynamic>))
          .toList();
      return TranslationRegistry(
        defaultTranslationId:
            data['defaultTranslationId'] as String? ??
            AppConstants.defaultTranslationId,
        items: items,
      );
    } catch (_) {
      return fallback();
    }
  }

  static TranslationRegistry fallback() {
    return TranslationRegistry(
      defaultTranslationId: AppConstants.defaultTranslationId,
      items: _fallbackItems(),
    );
  }

  static List<TranslationInfo> _fallbackItems() {
    return const [
      TranslationInfo(
        id: 'bsb',
        name: 'Berean Standard Bible',
        lang: 'en',
        direction: TextDirection.ltr,
        assetDb: 'assets/bibles/bsb.sqlite',
        publicDomain: true,
      ),
      TranslationInfo(
        id: 'web',
        name: 'World English Bible',
        lang: 'en',
        direction: TextDirection.ltr,
        assetDb: 'assets/bibles/web.sqlite',
        publicDomain: true,
      ),
      TranslationInfo(
        id: 'kjv',
        name: 'King James Version',
        lang: 'en',
        direction: TextDirection.ltr,
        assetDb: 'assets/bibles/kjv.sqlite',
        publicDomain: true,
      ),
      TranslationInfo(
        id: 'pov',
        name: 'Persian Old Version',
        lang: 'fa',
        direction: TextDirection.rtl,
        assetDb: 'assets/bibles/pov.sqlite',
        publicDomain: true,
      ),
    ];
  }
}
