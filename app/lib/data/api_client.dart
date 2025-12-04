import 'package:dio/dio.dart';
import 'package:shared_preferences/shared_preferences.dart';

// Комментарий: простой класс для общения с backend через HTTP
class ApiClient {
  ApiClient(this.baseUrl) : _dio = Dio(BaseOptions(baseUrl: baseUrl));

  final String baseUrl;
  final Dio _dio;

  Future<Map<String, dynamic>> fetchStatus() async {
    final response = await _dio.get('/api/status');
    return response.data as Map<String, dynamic>;
  }

  Future<String> login(String email, String password) async {
    final response = await _dio.post('/api/auth/demo-login', data: {
      'email': email,
      'password': password,
    });
    final token = response.data['access_token'] as String;
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('token', token);
    return token;
  }
}
