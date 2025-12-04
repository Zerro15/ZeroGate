import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/api_client.dart';

// Комментарий: провайдер базового URL, чтобы легко менять адрес сервера
final apiBaseUrlProvider = StateProvider<String>((ref) => 'http://localhost:8000');

// Провайдер клиента API, обновляется при смене адреса
final apiClientProvider = Provider<ApiClient>((ref) {
  final baseUrl = ref.watch(apiBaseUrlProvider);
  return ApiClient(baseUrl);
});

// Стейт для статус-экрана
final statusProvider = FutureProvider<Map<String, dynamic>>((ref) async {
  final client = ref.watch(apiClientProvider);
  return client.fetchStatus();
});
