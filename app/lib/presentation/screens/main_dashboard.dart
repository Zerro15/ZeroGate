import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../domain/providers.dart';

class MainDashboard extends ConsumerWidget {
  const MainDashboard({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final statusAsync = ref.watch(statusProvider);
    return Scaffold(
      appBar: AppBar(
        title: const Text('ZerroGate Dashboard'),
      ),
      body: statusAsync.when(
        data: (data) => _StatusView(data: data),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (e, _) => Center(child: Text('Ошибка загрузки: $e')),
      ),
    );
  }
}

class _StatusView extends StatelessWidget {
  const _StatusView({required this.data});

  final Map<String, dynamic> data;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Статус сервера: ${data['status']}',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          const SizedBox(height: 8),
          Text('Версия: ${data['version']}'),
          Text('Время сервера: ${data['timestamp']}'),
          const SizedBox(height: 24),
          const Text(
            'Дальше здесь появятся карточки устройств и профилей. Пока это минимальный учебный дашборд.',
          ),
        ],
      ),
    );
  }
}
