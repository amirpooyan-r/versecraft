import 'package:flutter/material.dart';

class ControlsPanel extends StatelessWidget {
  const ControlsPanel({
    super.key,
    required this.selectVerseLabel,
    required this.translationLabel,
    required this.layoutLabel,
    required this.exportLabel,
    this.onSelectVerse,
    this.onSelectTranslation,
    this.onSelectLayout,
    this.onExport,
  });

  final String selectVerseLabel;
  final String translationLabel;
  final String layoutLabel;
  final String exportLabel;
  final VoidCallback? onSelectVerse;
  final VoidCallback? onSelectTranslation;
  final VoidCallback? onSelectLayout;
  final VoidCallback? onExport;

  @override
  Widget build(BuildContext context) {
    return Wrap(
      spacing: 12,
      runSpacing: 12,
      alignment: WrapAlignment.center,
      children: [
        OutlinedButton(onPressed: onSelectVerse, child: Text(selectVerseLabel)),
        OutlinedButton(
          onPressed: onSelectTranslation,
          child: Text(translationLabel),
        ),
        OutlinedButton(onPressed: onSelectLayout, child: Text(layoutLabel)),
        FilledButton(onPressed: onExport, child: Text(exportLabel)),
      ],
    );
  }
}
