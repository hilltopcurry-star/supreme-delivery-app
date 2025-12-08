import 'package:flutter/material.dart';
 import 'package:http/http.dart' as http;
 import 'dart:convert';
 

 class DriverHomeScreen extends StatefulWidget {
  @override
  _DriverHomeScreenState createState() => _DriverHomeScreenState();
 }
 

 class _DriverHomeScreenState extends State<DriverHomeScreen> {
  bool _isOnline = false;
  List<dynamic> _jobRequests = [];
 

  @override
  void initState() {
  super.initState();
  _loadJobRequests();
  }
 

  Future<void> _toggleOnlineStatus() async {
  setState(() {
  _isOnline = !_isOnline;
  });
 

  // Simulate API call to update online status
  final url = Uri.parse('http://10.0.2.2:5000/driver/online_status');
  final response = await http.post(
  url,
  body: {'online': _isOnline.toString()},
  );
 

  if (response.statusCode == 200) {
  print('Online status updated successfully');
  } else {
  print('Failed to update online status');
  }
  }
 

  Future<void> _loadJobRequests() async {
  final url = Uri.parse('http://10.0.2.2:5000/driver/job_requests');
  final response = await http.get(url);
 

  if (response.statusCode == 200) {
  setState(() {
  _jobRequests = jsonDecode(response.body);
  });
  } else {
  print('Failed to load job requests');
  }
  }
 

  Future<void> _acceptJob(int jobId) async {
  final url = Uri.parse('http://10.0.2.2:5000/driver/accept_job');
  final response = await http.post(
  url,
  body: {'job_id': jobId.toString()},
  );
 

  if (response.statusCode == 200) {
  print('Job accepted successfully');
  _loadJobRequests(); // Refresh job requests
  } else {
  print('Failed to accept job');
  }
  }
 

  Future<void> _rejectJob(int jobId) async {
  final url = Uri.parse('http://10.0.2.2:5000/driver/reject_job');
  final response = await http.post(
  url,
  body: {'job_id': jobId.toString()},
  );
 

  if (response.statusCode == 200) {
  print('Job rejected successfully');
  _loadJobRequests(); // Refresh job requests
  } else {
  print('Failed to reject job');
  }
  }
 

  @override
  Widget build(BuildContext context) {
  return Scaffold(
  appBar: AppBar(
  title: Text('Driver Home'),
  actions: [
  Padding(
  padding: const EdgeInsets.all(8.0),
  child: ElevatedButton(
  onPressed: _toggleOnlineStatus,
  style: ElevatedButton.styleFrom(
  backgroundColor: _isOnline ? Colors.green : Colors.red,
  ),
  child: Text(_isOnline ? 'Online' : 'Offline'),
  ),
  ),
  ],
  ),
  body: _jobRequests.isEmpty
  ? Center(child: Text('No new job requests.'))
  : ListView.builder(
  itemCount: _jobRequests.length,
  itemBuilder: (context, index) {
  final job = _jobRequests[index];
  return Card(
  margin: EdgeInsets.all(8.0),
  child: Padding(
  padding: const EdgeInsets.all(16.0),
  child: Column(
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [
  Text('Job ID: ${job['id']}', style: TextStyle(fontWeight: FontWeight.bold)),
  Text('Pickup: ${job['pickup_location']}'),
  Text('Delivery: ${job['delivery_location']}'),
  Text('Amount: \$${job['amount']}'),
  Row(
  mainAxisAlignment: MainAxisAlignment.end,
  children: [
  ElevatedButton(
  onPressed: () => _acceptJob(job['id']),
  style: ElevatedButton.styleFrom(backgroundColor: Colors.green),
  child: Text('Accept'),
  ),
  SizedBox(width: 8.0),
  ElevatedButton(
  onPressed: () => _rejectJob(job['id']),
  style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
  child: Text('Reject'),
  ),
  ],
  ),
  ],
  ),
  ),
  );
  },
  ),
  );
  }
 }