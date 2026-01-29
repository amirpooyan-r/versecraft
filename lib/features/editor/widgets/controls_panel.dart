import 'package:flutter/material.dart';

class ControlsPanel extends StatelessWidget {
  const ControlsPanel({
    super.key,
    required this.selectVerseLabel,
    required this.translationLabel,
    required this.layoutLabel,
    required this.exportLabel,
  });

  final String selectVerseLabel;
  final String translationLabel;
  final String layoutLabel;
  final String exportLabel;

  @override
  Widget build(BuildContext context) {
    return Wrap(
      spacing: 12,
      runSpacing: 12,
      alignment: WrapAlignment.center,
      children: [
        OutlinedButton(onPressed: () {}, child: Text(selectVerseLabel)),
        OutlinedButton(onPressed: () {}, child: Text(translationLabel)),
        OutlinedButton(onPressed: () {}, child: Text(layoutLabel)),
        FilledButton(onPressed: () {}, child: Text(exportLabel)),
      ],
    );
  }
}
