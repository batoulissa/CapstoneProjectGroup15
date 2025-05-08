//
//  AdminLoginView.swift
//  TheraTalk-Frontend
//
//  Created by Sanna on 2025-02-02.
//

import Foundation
import SwiftUI

struct AdminLoginView: View {
    @State private var username = ""
    @State private var password = ""
    @State private var loginStatusMessage = ""
    @State private var isLoginSuccessful = false
    @State private var navigateToDashboard = false  // To control navigation to Admin Dashboard
    @State private var isLoggedIn = false  // Track if the admin is logged in

    var body: some View {
        NavigationStack {
            VStack {
                Text("Admin Login")
                    .font(.largeTitle)
                    .padding()

                TextField("Username", text: $username)
                    .padding()
                    .textFieldStyle(RoundedBorderTextFieldStyle())

                SecureField("Password", text: $password)
                    .padding()
                    .textFieldStyle(RoundedBorderTextFieldStyle())

                Button(action: {
                    loginAdmin(username: username, password: password)
                }) {
                    Text("Login")
                        .font(.title2)
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(8)
                }

                // Display status message if available
                if !loginStatusMessage.isEmpty {
                    Text(loginStatusMessage)
                        .foregroundColor(isLoginSuccessful ? .green : .red)
                        .padding()
                }

                Spacer()
                }
                .padding()
                .navigationTitle("Admin Login")
                // Use navigationDestination to navigate when login is successful
                .navigationDestination(isPresented: $navigateToDashboard) {
                    AdminDashboardView()
                }
        }
    }

    // Function to handle admin login
    func loginAdmin(username: String, password: String) {
        guard !username.isEmpty, !password.isEmpty else {
            loginStatusMessage = "Please enter both username and password"
            isLoginSuccessful = false
            return
        }

        let url = URL(string: "http://127.0.0.1:5000/admin/login_admin")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let payload: [String: Any] = [
            "username": username,
            "password": password
        ]

        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: payload, options: [])
        } catch {
            loginStatusMessage = "Error creating request: \(error.localizedDescription)"
            isLoginSuccessful = false
            return
        }

        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                DispatchQueue.main.async {
                    self.loginStatusMessage = "Login failed: \(error.localizedDescription)"
                    self.isLoginSuccessful = false
                }
                return
            }

            guard let data = data else {
                DispatchQueue.main.async {
                    self.loginStatusMessage = "No data received."
                    self.isLoginSuccessful = false
                }
                return
            }

            do {
                let responseJSON = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any]
                if let message = responseJSON?["message"] as? String {
                    DispatchQueue.main.async {
                        if message == "Login successful!" {
                            self.loginStatusMessage = message
                            self.isLoginSuccessful = true
                            self.isLoggedIn = true  // Set login status
                            self.navigateToDashboard = true  // Trigger navigation to Admin Dashboard
                        } else {
                            self.loginStatusMessage = message
                            self.isLoginSuccessful = false
                        }
                    }
                }
            } catch {
                DispatchQueue.main.async {
                    self.loginStatusMessage = "Failed to parse response: \(error.localizedDescription)"
                    self.isLoginSuccessful = false
                }
            }
        }

        task.resume()
    }

    // Function to handle admin logout
    func logoutAdmin() {
        self.isLoggedIn = false
        self.navigateToDashboard = false
        self.username = ""
        self.password = ""
        self.loginStatusMessage = "Logged out successfully."
    }
}

struct AdminLoginView_Previews: PreviewProvider {
    static var previews: some View {
        AdminLoginView()
    }
}
