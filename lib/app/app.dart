import 'package:flutter/material.dart';

import '../core/constants.dart';
import '../features/editor/editor_page.dart';
import 'routes.dart';
import 'theme.dart';

class VerseCraftApp extends StatelessWidget {
  const VerseCraftApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: AppConstants.appName,
      theme: buildAppTheme(),
      routes: AppRoutes.routes,
      initialRoute: AppRoutes.editor,
      onUnknownRoute: (_) =>
          MaterialPageRoute<void>(builder: (_) => const EditorPage()),
    );
  }
}
