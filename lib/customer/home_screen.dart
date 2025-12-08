import 'package:flutter/material.dart';
 import 'package:http/http.dart' as http;
 import 'dart:convert';

 class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
 }

 class _HomeScreenState extends State<HomeScreen> {
  List<String> categories = ['Pizza', 'Burgers', 'Sushi', 'Pasta', 'Salads'];
  List<Map<String, dynamic>> restaurants = [];

  @override
  void initState() {
  super.initState();
  fetchRestaurants();
  }

  Future<void> fetchRestaurants() async {
  final response = await http.get(Uri.parse('http://10.0.2.2:5000/restaurants')); // Replace with actual API endpoint
  if (response.statusCode == 200) {
  setState(() {
  restaurants = List<Map<String, dynamic>>.from(jsonDecode(response.body));
  });
  } else {
  // Handle error
  print('Failed to load restaurants: ${response.statusCode}');
  }
  }

  @override
  Widget build(BuildContext context) {
  return Scaffold(
  appBar: AppBar(
  title: Text('Supreme Delivery'),
  ),
  body: Column(
  children: [
  // Category List
  Container(
  height: 50,
  child: ListView.builder(
  scrollDirection: Axis.horizontal,
  itemCount: categories.length,
  itemBuilder: (context, index) {
  return Padding(
  padding: const EdgeInsets.all(8.0),
  child: Chip(
  label: Text(categories[index]),
  ),
  );
  },
  ),
  ),
  // Restaurant List
  Expanded(
  child: ListView.builder(
  itemCount: restaurants.length,
  itemBuilder: (context, index) {
  final restaurant = restaurants[index];
  return Card(
  margin: EdgeInsets.all(8.0),
  child: Padding(
  padding: const EdgeInsets.all(8.0),
  child: Column(
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [
  Text(
  restaurant['name'] ?? 'Restaurant Name',
  style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
  ),
  SizedBox(height: 4),
  Text(restaurant['cuisine'] ?? 'Cuisine Type'),
  SizedBox(height: 4),
  Text('Rating: ${restaurant['rating'] ?? 'N/A'}'),
  ],
  ),
  ),
  );
  },
  ),
  ),
  ],
  ),
  bottomNavigationBar: BottomNavigationBar(
  items: const <BottomNavigationBarItem>[
  BottomNavigationBarItem(
  icon: Icon(Icons.home),
  label: 'Home',
  ),
  BottomNavigationBarItem(
  icon: Icon(Icons.search),
  label: 'Search',
  ),
  BottomNavigationBarItem(
  icon: Icon(Icons.shopping_cart),
  label: 'Cart',
  ),
  BottomNavigationBarItem(
  icon: Icon(Icons.person),
  label: 'Profile',
  ),
  ],
  ),
  );
  }
 }