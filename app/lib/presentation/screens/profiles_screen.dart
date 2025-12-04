import 'package:flutter/material.dart';

/// Заглушка экрана профилей подключений.
class ProfilesScreen extends StatelessWidget {
  const ProfilesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      appBar: AppBar(title: Text('Профили подключений')),
      body: Center(child: Text('Здесь будет управление профилями.')),
    );
  }
}
