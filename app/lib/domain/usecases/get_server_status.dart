import '../../data/repositories/status_repository.dart';
import '../entities/server_status.dart';

/// Юзкейс получения статуса сервера.
class GetServerStatus {
  GetServerStatus(this._repository);

  final StatusRepository _repository;

  Future<ServerStatus> call() {
    return _repository.loadStatus();
  }
}
