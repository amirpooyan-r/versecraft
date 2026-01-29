import 'package:flutter/material.dart';

import '../../core/utils/text_direction.dart';
import '../../i18n/l10n.dart';
import 'widgets/controls_panel.dart';
import 'widgets/verse_card.dart';

class EditorPage extends StatelessWidget {
  const EditorPage({super.key});

  @override
  Widget build(BuildContext context) {
    final strings = L10n.strings;
    final textDirection = AppTextDirection.forLocale(L10n.locale);

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
                        reference: 'John 3:16',
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
              ),
            ],
          ),
        ),
      ),
    );
  }
}
