import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../data/repositories/status_repository.dart';
import '../../domain/entities/server_status.dart';
import '../../domain/usecases/get_server_status.dart';
import 'auth_providers.dart';

/// Провайдер репозитория статуса.
final statusRepositoryProvider = Provider<StatusRepository>((ref) {
  final client = ref.watch(apiClientProvider);
  return StatusRepository(client);
});

/// Провайдер юзкейса статуса.
final getStatusUseCaseProvider = Provider<GetServerStatus>((ref) {
  final repo = ref.watch(statusRepositoryProvider);
  return GetServerStatus(repo);
});

/// Провайдер, который реально грузит статус и даёт Future в UI.
final serverStatusProvider = FutureProvider<ServerStatus>((ref) async {
  final useCase = ref.watch(getStatusUseCaseProvider);
  return useCase();
});
