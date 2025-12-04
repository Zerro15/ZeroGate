import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../../core/app_config.dart';
import '../../data/api_client.dart';
import '../../data/repositories/auth_repository.dart';
import '../../domain/usecases/login_user.dart';

/// Провайдер конфигурации приложения.
final appConfigProvider = Provider<AppConfig>((ref) => AppConfig());

/// Провайдер HTTP-клиента, который реагирует на изменение baseUrl.
final apiClientProvider = Provider<ApiClient>((ref) {
  final baseUrl = ref.watch(appConfigProvider).baseUrl;
  return ApiClient(baseUrl);
});

/// Провайдер репозитория авторизации.
final authRepositoryProvider = Provider<AuthRepository>((ref) {
  final client = ref.watch(apiClientProvider);
  return AuthRepository(client);
});

/// Провайдер юзкейса логина.
final loginUserProvider = Provider<LoginUser>((ref) {
  final repo = ref.watch(authRepositoryProvider);
  return LoginUser(repo);
});

/// Состояние авторизации: храним токен, чтобы UI знал, вошёл ли пользователь.
class AuthState {
  const AuthState({this.token, this.isLoading = false, this.error});

  final String? token;
  final bool isLoading;
  final String? error;

  AuthState copyWith({String? token, bool? isLoading, String? error}) {
    return AuthState(
      token: token ?? this.token,
      isLoading: isLoading ?? this.isLoading,
      error: error,
    );
  }
}

class AuthNotifier extends StateNotifier<AuthState> {
  AuthNotifier(this._login) : super(const AuthState());

  final LoginUser _login;

  Future<void> login(String email, String password) async {
    state = state.copyWith(isLoading: true, error: null);
    try {
      final token = await _login(email, password);
      state = state.copyWith(token: token, isLoading: false);
    } catch (e) {
      state = state.copyWith(error: 'Не удалось войти: $e', isLoading: false);
    }
  }
}

final authNotifierProvider = StateNotifierProvider<AuthNotifier, AuthState>((ref) {
  final loginUser = ref.watch(loginUserProvider);
  return AuthNotifier(loginUser);
});
