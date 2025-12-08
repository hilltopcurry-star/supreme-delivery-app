import 'dart:convert';
 import 'package:http/http.dart' as http;
 import 'package:shared_preferences/shared_preferences.dart';

 class ApiService {
  static const String baseUrl = 'http://10.0.2.2:5000';

  static Future<Map<String, dynamic>> login(String username, String password) async {
  final response = await http.post(
  Uri.parse('$baseUrl/auth/login'),
  headers: <String, String>{
  'Content-Type': 'application/json; charset=UTF-8',
  },
  body: jsonEncode(<String, String>{
  'username': username,
  'password': password,
  }),
  );

  if (response.statusCode == 200) {
  final responseData = jsonDecode(response.body);
  if (responseData.containsKey('token')) {
  SharedPreferences prefs = await SharedPreferences.getInstance();
  await prefs.setString('token', responseData['token']);
  }
  return responseData;
  } else {
  throw Exception('Failed to login: ${response.statusCode}');
  }
  }

  static Future<List<dynamic>> fetchRestaurants() async {
  SharedPreferences prefs = await SharedPreferences.getInstance();
  final String? token = prefs.getString('token');

  final response = await http.get(
  Uri.parse('$baseUrl/restaurants'),
  headers: <String, String>{
  'Content-Type': 'application/json; charset=UTF-8',
  'Authorization': 'Bearer $token',
  },
  );

  if (response.statusCode == 200) {
  return jsonDecode(response.body);
  } else {
  throw Exception('Failed to fetch restaurants: ${response.statusCode}');
  }
  }

  static Future<Map<String, dynamic>> placeOrder(Map<String, dynamic> orderData) async {
  SharedPreferences prefs = await SharedPreferences.getInstance();
  final String? token = prefs.getString('token');

  final response = await http.post(
  Uri.parse('$baseUrl/orders'),
  headers: <String, String>{
  'Content-Type': 'application/json; charset=UTF-8',
  'Authorization': 'Bearer $token',
  },
  body: jsonEncode(orderData),
  );

  if (response.statusCode == 201) {
  return jsonDecode(response.body);
  } else {
  throw Exception('Failed to place order: ${response.statusCode}');
  }
  }

  static Future<void> updateDriverLocation(String driverId, double latitude, double longitude) async {
  SharedPreferences prefs = await SharedPreferences.getInstance();
  final String? token = prefs.getString('token');

  final response = await http.post(
  Uri.parse('$baseUrl/drivers/$driverId/location'),
  headers: <String, String>{
  'Content-Type': 'application/json; charset=UTF-8',
  'Authorization': 'Bearer $token',
  },
  body: jsonEncode(<String, dynamic>{
  'latitude': latitude,
  'longitude': longitude,
  }),
  );

  if (response.statusCode != 200) {
  throw Exception('Failed to update driver location: ${response.statusCode}');
  }
  }
 }