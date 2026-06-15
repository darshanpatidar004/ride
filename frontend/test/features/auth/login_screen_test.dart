import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:ride_app/features/auth/presentation/screens/login_screen.dart';

void main() {
  testWidgets('Login screen has essential fields and button', (WidgetTester tester) async {
    // Build our app and trigger a frame.
    await tester.pumpWidget(const MaterialApp(home: LoginScreen()));

    // Verify presence of UI elements
    expect(find.text('Welcome to Quick Ride'), findsOneWidget);
    expect(find.byType(TextFormField), findsNWidgets(2));
    expect(find.text('Email or Phone Number'), findsOneWidget);
    expect(find.text('Password'), findsOneWidget);
    expect(find.byType(ElevatedButton), findsOneWidget);
    expect(find.text('Login'), findsOneWidget);
  });
}
