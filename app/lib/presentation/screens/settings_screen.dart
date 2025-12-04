import 'package:flutter/material.dart';

/// Заглушка экрана настроек.
class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      appBar: AppBar(title: Text('Настройки')),
      body: Center(child: Text('Настройки (тема, язык, адрес backend) будут здесь.')),
    );
  }
}
