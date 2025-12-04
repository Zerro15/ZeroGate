import '../../data/repositories/auth_repository.dart';

/// Юзкейс для логина пользователя.
class LoginUser {
  LoginUser(this._repository);

  final AuthRepository _repository;

  Future<String> call(String email, String password) {
    return _repository.login(email, password);
  }
}
