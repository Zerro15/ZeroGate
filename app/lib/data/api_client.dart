import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Простой HTTP-клиент для общения с backend.
/// Комментарии на русском, чтобы новичку было понятно.
class ApiClient {
  ApiClient(String baseUrl)
      : _dio = Dio(
          BaseOptions(
            baseUrl: baseUrl,
            connectTimeout: const Duration(seconds: 5),
            receiveTimeout: const Duration(seconds: 5),
          ),
        );

  final Dio _dio;

  /// Обновляем базовый URL, если пользователь поменял адрес backend.
  void updateBaseUrl(String baseUrl) {
    _dio.options.baseUrl = baseUrl;
  }

  /// Логин через OAuth2 password flow (формат, который ожидает FastAPI).
  Future<String> login(String email, String password) async {
    final response = await _dio.post(
      '/api/auth/login',
      data: {'username': email, 'password': password},
      options: Options(contentType: Headers.formUrlEncodedContentType),
    );
    final token = response.data['access_token'] as String;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('token', token);
    _dio.options.headers['Authorization'] = 'Bearer $token';
    return token;
  }

  /// Запрашиваем статус сервера.
  Future<Map<String, dynamic>> fetchStatus() async {
    final response = await _dio.get('/api/status');
    return response.data as Map<String, dynamic>;
  }
}
