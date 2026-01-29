import 'package:flutter/material.dart';

class VerseCard extends StatelessWidget {
  const VerseCard({
    super.key,
    required this.textDirection,
    required this.verseText,
    required this.reference,
  });

  final TextDirection textDirection;
  final String verseText;
  final String reference;

  @override
  Widget build(BuildContext context) {
    return Directionality(
      textDirection: textDirection,
      child: Container(
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(
          color: const Color(0xFFE7E4DD),
          borderRadius: BorderRadius.circular(20),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(
              verseText,
              textAlign: TextAlign.center,
              style: Theme.of(
                context,
              ).textTheme.titleLarge?.copyWith(height: 1.4),
            ),
            const SizedBox(height: 16),
            Text(
              reference,
              style: Theme.of(
                context,
              ).textTheme.titleMedium?.copyWith(fontWeight: FontWeight.w600),
            ),
          ],
        ),
      ),
    );
  }
}
