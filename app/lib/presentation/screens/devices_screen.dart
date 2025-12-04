import 'package:flutter/material.dart';

/// Заглушка экрана устройств. Позже здесь будет список устройств из API.
class DevicesScreen extends StatelessWidget {
  const DevicesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      appBar: AppBar(title: Text('Устройства')),
      body: Center(child: Text('Список устройств появится в следующих версиях.')),
    );
  }
}
