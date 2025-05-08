//
//  LoginView.swift
//  TheraTalk-Frontend
//
//  Created by Sanna on 2025-02-02.
//

import Foundation
import SwiftUI

struct LoginView: View {
    @State private var name: String = ""
    @State private var password: String = ""
    @State private var selectedRole: String = "Patient"
    @State private var showError: Bool = false
    @State private var errorMessage: String = ""
    @State private var navigateToDashboard = false
    
    let roles = ["Patient", "Therapist"]
    
    var body: some View {
        NavigationStack{
            VStack {
                Text("Login")
                    .font(.largeTitle)
                    .padding()
                
                TextField("Name", text: $name)  // Updated field to 'Name'
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()
                    .autocapitalization(.words)  // Auto capitalize first letter of name
                
                SecureField("Password", text: $password)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()
                
                Picker("Select Role", selection: $selectedRole) {
                    ForEach(roles, id: \.self) { role in
                        Text(role)
                    }
                }
                .pickerStyle(SegmentedPickerStyle())
                .padding()
                
                Button(action: loginAction) {
                    Text("Login")
                        .font(.title2)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color.orange)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                        .padding(.horizontal)
                }
                
                if showError {
                    Text(errorMessage)
                        .foregroundColor(.red)
                        .padding()
                }
                NavigationLink(destination: getDashboard()) {
                    EmptyView()
                }
            }
            .navigationTitle("Login")
        }
    }
        
        func loginAction() {
            // Validate name and password
            if name.isEmpty || password.isEmpty {
                showError = true
                errorMessage = "⚠️ Please fill in all fields"
                return
            }
            
            // Make API call here for login with selectedRole, name, and password
            loginUser()
        }
        
        func loginUser() {
            // Make a request to the backend API
            let url = URL(string: "https://yourapi.com/login")! // Update the URL as necessary
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            let body = [
                "name": name,  // Send the 'name' field
                "password": password,
                "role": selectedRole
            ]
            
            do {
                request.httpBody = try JSONSerialization.data(withJSONObject: body)
            } catch {
                showError = true
                errorMessage = "⚠️ Failed to create request"
                return
            }
            
            let task = URLSession.shared.dataTask(with: request) { data, response, error in
                if let error = error {
                    DispatchQueue.main.async {
                        showError = true
                        errorMessage = "⚠️ Network error: \(error.localizedDescription)"
                    }
                    return
                }
                
                guard let data = data else {
                    DispatchQueue.main.async {
                        showError = true
                        errorMessage = "⚠️ No data received"
                    }
                    return
                }
                
                // Parse the response from the backend
                if let responseJSON = try? JSONDecoder().decode(LoginResponse.self, from: data) {
                    DispatchQueue.main.async {
                        if responseJSON.message == "Login successful!" {
                            navigateToDashboard = true
                        } else {
                            showError = true
                            errorMessage = responseJSON.message
                        }
                    }
                } else {
                    DispatchQueue.main.async {
                        showError = true
                        errorMessage = "⚠️ Invalid credentials"
                    }
                }
            }
            task.resume()
        }
        
        @ViewBuilder
        func getDashboard() -> some View {
            switch selectedRole {
            case "Patient":
                PatientDashboardView()
            case "Therapist":
                TherapistDashboardView()
            default:
                Text("Invalid Role")
            }
        }
    }
    
    struct LoginResponse: Codable {
        let message: String
    }

