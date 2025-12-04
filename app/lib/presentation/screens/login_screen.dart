import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../providers/auth_providers.dart';
import '../providers/status_providers.dart';
import 'status_screen.dart';

/// Экран логина: пользователь вводит backend URL, email и пароль.
class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key, required this.onToggleTheme});

  final VoidCallback onToggleTheme;

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController(text: 'admin@zerogate.local');
  final _passwordController = TextEditingController(text: 'admin');
  final _baseUrlController = TextEditingController(text: 'http://localhost:8000');

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    _baseUrlController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    if (!_formKey.currentState!.validate()) return;
    // Обновляем базовый URL для API-клиента
    ref.read(apiClientProvider).updateBaseUrl(_baseUrlController.text.trim());

    await ref.read(authNotifierProvider.notifier).login(
          _emailController.text.trim(),
          _passwordController.text.trim(),
        );
    final authState = ref.read(authNotifierProvider);
    if (authState.error != null) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(authState.error!)),
      );
      return;
    }
    if (authState.token != null && mounted) {
      // Навигация на экран статуса
      Navigator.of(context).pushReplacementNamed(StatusScreen.routeName);
      // Подгружаем статус сразу после входа
      ref.invalidate(serverStatusProvider);
    }
  }

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authNotifierProvider);
    return Scaffold(
      appBar: AppBar(
        title: const Text('ZeroGate вход'),
        actions: [
          IconButton(
            icon: const Icon(Icons.wb_sunny_outlined),
            onPressed: widget.onToggleTheme,
          )
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              TextFormField(
                controller: _baseUrlController,
                decoration: const InputDecoration(labelText: 'Адрес backend'),
                validator: (v) => v == null || v.isEmpty ? 'Введите адрес' : null,
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _emailController,
                decoration: const InputDecoration(labelText: 'Email'),
                validator: (v) => v == null || v.isEmpty ? 'Email обязателен' : null,
              ),
              const SizedBox(height: 12),
              TextFormField(
                controller: _passwordController,
                decoration: const InputDecoration(labelText: 'Пароль'),
                obscureText: true,
                validator: (v) => v == null || v.isEmpty ? 'Пароль обязателен' : null,
              ),
              const SizedBox(height: 18),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: authState.isLoading ? null : _submit,
                  child: authState.isLoading
                      ? const SizedBox(
                          width: 18,
                          height: 18,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Text('Войти и открыть дашборд'),
                ),
              ),
              const SizedBox(height: 16),
              const Text(
                'Подсказка: логин admin@zerogate.local / пароль admin создаются автоматически.',
              ),
            ],
          ),
        ),
      ),
    );
  }
}
