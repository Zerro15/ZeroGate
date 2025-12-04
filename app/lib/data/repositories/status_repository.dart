import '../api_client.dart';
import '../../domain/entities/server_status.dart';

/// Репозиторий статуса сервера.
class StatusRepository {
  StatusRepository(this._client);

  final ApiClient _client;

  Future<ServerStatus> loadStatus() async {
    final data = await _client.fetchStatus();
    return ServerStatus.fromJson(data);
  }
}
