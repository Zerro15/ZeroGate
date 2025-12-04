/// Простая модель ответа статуса сервера.
class ServerStatus {
  ServerStatus({required this.project, required this.status, required this.timestamp});

  final String project;
  final String status;
  final String timestamp;

  factory ServerStatus.fromJson(Map<String, dynamic> json) {
    return ServerStatus(
      project: json['project'] as String? ?? 'Unknown',
      status: json['status'] as String? ?? 'unknown',
      timestamp: json['timestamp'] as String? ?? '',
    );
  }
}
