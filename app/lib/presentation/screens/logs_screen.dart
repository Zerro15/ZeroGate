import 'package:flutter/material.dart';

/// Заглушка экрана логов.
class LogsScreen extends StatelessWidget {
  const LogsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      appBar: AppBar(title: Text('Логи')),
      body: Center(child: Text('Отображение логов появится позже.')),
    );
  }
}
