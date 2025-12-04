import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'presentation/providers/auth_providers.dart';
import 'presentation/screens/login_screen.dart';
import 'presentation/screens/status_screen.dart';

void main() {
  // ProviderScope инициализирует Riverpod, чтобы стейт был доступен во всём приложении
  runApp(const ProviderScope(child: ZeroGateApp()));
}

class ZeroGateApp extends StatefulWidget {
  const ZeroGateApp({super.key});

  @override
  State<ZeroGateApp> createState() => _ZeroGateAppState();
}

class _ZeroGateAppState extends State<ZeroGateApp> {
  ThemeMode _themeMode = ThemeMode.system;

  void _toggleTheme() {
    setState(() {
      _themeMode = _themeMode == ThemeMode.light ? ThemeMode.dark : ThemeMode.light;
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ZeroGate',
      themeMode: _themeMode,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.indigo),
        useMaterial3: true,
      ),
      darkTheme: ThemeData.dark(useMaterial3: true),
      home: LoginScreen(onToggleTheme: _toggleTheme),
      routes: {
        StatusScreen.routeName: (_) => const StatusScreen(),
      },
    );
  }
}
