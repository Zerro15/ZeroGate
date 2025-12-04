import '../api_client.dart';

/// Репозиторий авторизации изолирует детали HTTP от остального кода.
class AuthRepository {
  AuthRepository(this._client);

  final ApiClient _client;

  Future<String> login(String email, String password) {
    // Возвращаем токен, чтобы стор мог сохранить его в состоянии
    return _client.login(email, password);
  }
}
