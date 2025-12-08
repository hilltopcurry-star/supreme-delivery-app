import 'package:flutter/material.dart';
 import 'package:http/http.dart' as http;
 import 'dart:convert';
 

 class HomeScreen extends StatefulWidget {
  @override
  _HomeScreenState createState() => _HomeScreenState();
 }
 

 class _HomeScreenState extends State<HomeScreen> {
  List<dynamic> categories = [];
  List<dynamic> restaurants = [];
 

  @override
  void initState() {
  super.initState();
  fetchCategories();
  fetchRestaurants();
  }
 

  Future<void> fetchCategories() async {
  final response = await http.get(Uri.parse('http://10.0.2.2:5000/api/categories'));
  if (response.statusCode == 200) {
  setState(() {
  categories = jsonDecode(response.body);
  });
  } else {
  print('Failed to load categories');
  }
  }
 

  Future<void> fetchRestaurants() async {
  final response = await http.get(Uri.parse('http://10.0.2.2:5000/api/restaurants'));
  if (response.statusCode == 200) {
  setState(() {
  restaurants = jsonDecode(response.body);
  });
  } else {
  print('Failed to load restaurants');
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
  height: 80,
  child: ListView.builder(
  scrollDirection: Axis.horizontal,
  itemCount: categories.length,
  itemBuilder: (context, index) {
  return Padding(
  padding: const EdgeInsets.all(8.0),
  child: Chip(
  label: Text(categories[index]['name']),
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
  return Card(
  margin: EdgeInsets.all(8.0),
  child: Padding(
  padding: const EdgeInsets.all(8.0),
  child: Column(
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [
  Text(
  restaurants[index]['name'],
  style: TextStyle(
  fontSize: 18,
  fontWeight: FontWeight.bold,
  ),
  ),
  SizedBox(height: 4),
  Text(restaurants[index]['cuisine']),
  SizedBox(height: 4),
  Text('Rating: ${restaurants[index]['rating']}'),
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
  selectedItemColor: Colors.blue,
  unselectedItemColor: Colors.grey,
  ),
  );
  }
 }