import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'presentation/screens/login_screen.dart';

void main() {
  // Комментарий: ProviderScope инициализирует Riverpod, чтобы стейт был доступен
  runApp(const ProviderScope(child: ZerroGateApp()));
}

class ZerroGateApp extends StatefulWidget {
  const ZerroGateApp({super.key});

  @override
  State<ZerroGateApp> createState() => _ZerroGateAppState();
}

class _ZerroGateAppState extends State<ZerroGateApp> {
  ThemeMode _themeMode = ThemeMode.system;

  void _toggleTheme() {
    setState(() {
      _themeMode = _themeMode == ThemeMode.light ? ThemeMode.dark : ThemeMode.light;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ZerroGate',
      themeMode: _themeMode,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
      ),
      darkTheme: ThemeData.dark(useMaterial3: true),
      home: LoginScreen(onToggleTheme: _toggleTheme),
    );
  }
}
