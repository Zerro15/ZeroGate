/// Конфиг приложения с базовыми настройками.
class AppConfig {
  AppConfig({this.baseUrl = 'http://localhost:8000'});

  /// Адрес backend по умолчанию
  final String baseUrl;
}
