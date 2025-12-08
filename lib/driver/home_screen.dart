import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

class DriverHomeScreen extends StatefulWidget {
  @override
  _DriverHomeScreenState createState() => _DriverHomeScreenState();
}

class _DriverHomeScreenState extends State<DriverHomeScreen> {
  bool _isOnline = false;
  List<dynamic> _jobRequests = [];
  String? _authToken;

  @override
  void initState() {
    super.initState();
    _loadAuthToken();
  }

  Future<void> _loadAuthToken() async {
    final prefs = await SharedPreferences.getInstance();
    setState(() {
      _authToken = prefs.getString('auth_token');
      if (_authToken != null) {
        _fetchJobRequests();
      } else {
        // Handle the case where the auth token is missing.  Maybe redirect to login.
        print('Auth token not found. Redirect to login.'); // Replace with proper navigation.
      }
    });
  }


  Future<void> _fetchJobRequests() async {
    final url = Uri.parse('http://10.0.2.2:5000/driver/job_requests'); // Replace with your API endpoint
    try {
      final response = await http.get(url, headers: {
        'Authorization': 'Bearer $_authToken',
      });

      if (response.statusCode == 200) {
        setState(() {
          _jobRequests = jsonDecode(response.body);
        });
      } else {
        print('Failed to fetch job requests: ${response.statusCode}');
        // Handle error (e.g., show a snackbar).
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to fetch job requests.')),
        );
      }
    } catch (e) {
      print('Error fetching job requests: $e');
      // Handle network errors.
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Network error fetching job requests.')),
      );
    }
  }

  Future<void> _updateOnlineStatus(bool isOnline) async {
    final url = Uri.parse('http://10.0.2.2:5000/driver/online_status'); // Replace with your API endpoint
    try {
      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $_authToken',
        },
        body: jsonEncode({'is_online': isOnline}),
      );

      if (response.statusCode == 200) {
        setState(() {
          _isOnline = isOnline;
        });
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Online status updated.')),
        );
      } else {
        print('Failed to update online status: ${response.statusCode}');
        // Handle error (e.g., show a snackbar).
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to update online status.')),
        );
      }
    } catch (e) {
      print('Error updating online status: $e');
      // Handle network errors.
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Network error updating online status.')),
      );
    }
  }

  Future<void> _acceptJob(int jobRequestId) async {
    final url = Uri.parse('http://10.0.2.2:5000/driver/accept_job'); // Replace with your API endpoint
    try {
      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $_authToken',
        },
        body: jsonEncode({'job_request_id': jobRequestId}),
      );

      if (response.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Job accepted.')),
        );
        _fetchJobRequests(); // Refresh job requests after accepting
      } else {
        print('Failed to accept job: ${response.statusCode}');
        // Handle error (e.g., show a snackbar).
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to accept job.')),
        );
      }
    } catch (e) {
      print('Error accepting job: $e');
      // Handle network errors.
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Network error accepting job.')),
      );
    }
  }

  Future<void> _rejectJob(int jobRequestId) async {
    final url = Uri.parse('http://10.0.2.2:5000/driver/reject_job'); // Replace with your API endpoint
    try {
      final response = await http.post(
        url,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $_authToken',
        },
        body: jsonEncode({'job_request_id': jobRequestId}),
      );

      if (response.statusCode == 200) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Job rejected.')),
        );
        _fetchJobRequests(); // Refresh job requests after rejecting
      } else {
        print('Failed to reject job: ${response.statusCode}');
        // Handle error (e.g., show a snackbar).
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Failed to reject job.')),
        );
      }
    } catch (e) {
      print('Error rejecting job: $e');
      // Handle network errors.
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Network error rejecting job.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Driver Home'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('Online Status: ${_isOnline ? 'Online' : 'Offline'}'),
                Switch(
                  value: _isOnline,
                  onChanged: (value) {
                    _updateOnlineStatus(value);
                  },
                ),
              ],
            ),
            SizedBox(height: 20),
            Text('New Job Requests:', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            Expanded(
              child: _jobRequests.isEmpty
                  ? Center(child: Text('No new job requests.'))
                  : ListView.builder(
                      itemCount: _jobRequests.length,
                      itemBuilder: (context, index) {
                        final jobRequest = _jobRequests[index];
                        return Card(
                          child: Padding(
                            padding: const EdgeInsets.all(8.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text('Request ID: ${jobRequest['id']}'),
                                Text('Pickup Location: ${jobRequest['pickup_location']}'),
                                Text('Delivery Location: ${jobRequest['delivery_location']}'),
                                Text('Customer Name: ${jobRequest['customer_name']}'), //example field
                                Row(
                                  mainAxisAlignment: MainAxisAlignment.end,
                                  children: [
                                    ElevatedButton(
                                      onPressed: () {
                                        _acceptJob(jobRequest['id']);
                                      },
                                      child: Text('Accept'),
                                    ),
                                    SizedBox(width: 10),
                                    ElevatedButton(
                                      onPressed: () {
                                        _rejectJob(jobRequest['id']);
                                      },
                                      child: Text('Reject'),
                                      style: ElevatedButton.styleFrom(backgroundColor: Colors.red),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }
}