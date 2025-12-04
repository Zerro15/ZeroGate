import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../providers/status_providers.dart';

/// Экран статуса сервера.
class StatusScreen extends ConsumerWidget {
  const StatusScreen({super.key});

  static const routeName = '/status';

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final statusAsync = ref.watch(serverStatusProvider);
    return Scaffold(
      appBar: AppBar(
        title: const Text('Статус сервера'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: statusAsync.when(
          data: (status) => Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Проект: ${status.project}', style: Theme.of(context).textTheme.titleLarge),
              const SizedBox(height: 8),
              Text('Статус: ${status.status}'),
              const SizedBox(height: 8),
              Text('Время: ${status.timestamp}'),
              const SizedBox(height: 12),
              FilledButton(
                onPressed: () => ref.refresh(serverStatusProvider),
                child: const Text('Обновить'),
              ),
            ],
          ),
          loading: () => const Center(child: CircularProgressIndicator()),
          error: (err, _) => Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Не удалось получить статус: $err'),
              const SizedBox(height: 12),
              FilledButton(
                onPressed: () => ref.refresh(serverStatusProvider),
                child: const Text('Повторить запрос'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
