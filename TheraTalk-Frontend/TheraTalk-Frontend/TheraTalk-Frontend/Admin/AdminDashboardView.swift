//
//  AdminDashboardView.swift
//  TheraTalk-Frontend
//
//  Created by Sanna on 2025-02-02.
//

import Foundation
import SwiftUI

// Admin Dashboard View
struct AdminDashboardView: View {
    @State private var pendingTherapists: [Therapist] = []
    @State private var approvedTherapists: [Therapist] = []
    @State private var navigateToLogin = false
    @State private var navigateToCreateAdmin = false // Navigate to create new admin page
    
    
    var body: some View {
        NavigationStack {
            VStack {
                Text("Admin Dashboard")
                    .font(.largeTitle)
                    .padding()
                
                Button(action: {
                    logoutAdmin()  // Call the logout function from AdminLoginView
                    navigateToLogin = true  // Redirect to login page
                }) {
                    Text("Logout")
                        .font(.title3)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color.red)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                        .padding(.horizontal)
                }
                
                // Create New Admin Button
                Button(action: {
                    navigateToCreateAdmin = true
                }) {
                    Text("Create New Admin")
                        .font(.title3)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                        .padding(.horizontal)
                }
                
                List {
                    Section(header: Text("Pending Therapists")) {
                        ForEach(pendingTherapists) { therapist in
                            therapistRow(therapist: therapist, isPending: true)
                        }
                    }
                    
                    Section(header: Text("Approved Therapists")) {
                        ForEach(approvedTherapists) { therapist in
                            therapistRow(therapist: therapist, isPending: false)
                        }
                    }
                }
                .onAppear {
                    fetchTherapists()
                }
                
                // NavigationLink to Admin Login Page
                NavigationLink(destination: AdminLoginView(), isActive: $navigateToLogin) {
                    EmptyView()
                }
                // NavigationLink to Admin Registration Page
                .navigationDestination(for: Bool.self) { _ in
                    AdminLoginView()
                }
                NavigationLink(value: navigateToCreateAdmin){
                    EmptyView()
                }
                .navigationDestination(for: Bool.self){ _ in
                    AdminRegistrationView()
                    
                }
            }
        }
    }
        
        // Function to display therapist row
        func therapistRow(therapist: Therapist, isPending: Bool) -> some View {
            HStack {
                VStack(alignment: .leading) {
                    Text(therapist.name)
                        .font(.headline)
                    Text("Status: \(therapist.status)")
                        .font(.subheadline)
                        .foregroundColor(therapist.status == "approved" ? .green : .orange)
                }
                Spacer()
                
                if isPending {
                    Button(action: {
                        approveTherapist(id: therapist.id)
                    }) {
                        Text("Approve")
                            .foregroundColor(.white)
                            .padding(8)
                            .background(Color.green)
                            .cornerRadius(8)
                    }
                    
                    Button(action: {
                        rejectTherapist(id: therapist.id)
                    }) {
                        Text("Reject")
                            .foregroundColor(.white)
                            .padding(8)
                            .background(Color.red)
                            .cornerRadius(8)
                    }
                }
            }
            .padding(5)
        }
        
        // Fetch both pending and approved therapists
        func fetchTherapists() {
            guard let url = URL(string: "http://127.0.0.1:5000/admin/get_all_therapists") else { return }
            
            URLSession.shared.dataTask(with: url) { data, response, error in
                if let data = data {
                    // Log the raw data for inspection
                    if let jsonString = String(data: data, encoding: .utf8) {
                        print("Raw JSON Response: \(jsonString)")
                    }
                    
                    do {
                        // Decode the therapists list
                        let decodedTherapists = try JSONDecoder().decode([Therapist].self, from: data)
                        DispatchQueue.main.async {
                            // Filter therapists by status (pending or approved)
                            pendingTherapists = decodedTherapists.filter { $0.status == "pending" }
                            approvedTherapists = decodedTherapists.filter { $0.status == "approved" }
                        }
                    } catch {
                        print("Failed to decode therapists list")
                    }
                } else if let error = error {
                    print("Error feting data: \(error.localizedDescription)")
                }
            }.resume()
        }
        
        // Approve a therapist
        func approveTherapist(id: Int) {
            sendTherapistUpdateRequest(id: id, endpoint: "approve_therapist")
        }
        
        // Reject a therapist
        func rejectTherapist(id: Int) {
            sendTherapistUpdateRequest(id: id, endpoint: "reject_therapist")
        }
        
        // Logout admin
        func logoutAdmin() {
            guard let url = URL(string: "http://127.0.0.1:5000/admin/logout_admin") else { return }
            
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")
            
            URLSession.shared.dataTask(with: request) { data, response, error in
                if let data = data {
                    do {
                        if let jsonResponse = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any] {
                            DispatchQueue.main.async {
                                print(jsonResponse["message"] ?? "Unknown response")
                                navigateToLogin = true  // Redirect to login after logout
                            }
                        }
                    } catch {
                        print("Failed to parse JSON response")
                    }
                }
            }.resume()
        }
        
        // Generic function to send approve/reject request
        func sendTherapistUpdateRequest(id: Int, endpoint: String) {
            guard let url = URL(string: "http://127.0.0.1:5000/\(endpoint)/\(id)") else { return }
            
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")
            
            URLSession.shared.dataTask(with: request) { data, response, error in
                if let data = data {
                    do {
                        if let jsonResponse = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any] {
                            DispatchQueue.main.async {
                                print(jsonResponse["message"] ?? "Unknown response")
                                fetchTherapists()  // Refresh the list
                            }
                        }
                    } catch {
                        print("Failed to parse JSON response")
                    }
                }
            }.resume()
        }
    }
    
    struct Therapist: Identifiable, Codable {
        let id: Int
        let name: String
        let experience_years: Int
        let availability: String
        let languages: String  // Decode JSON string to an array
        let focus_areas: String  // Decode JSON string to an array
        let proof_of_education: String
        let status: String
    }

    
    // Admin Registration View (For creating new admin)
    struct AdminRegistrationView: View {
        @State private var username = ""
        @State private var password = ""
        @State private var confirmPassword = ""
        @State private var registrationStatusMessage = ""
        
        var body: some View {
            VStack {
                Text("Create New Admin")
                    .font(.largeTitle)
                    .padding()
                
                TextField("Username", text: $username)
                    .padding()
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                
                SecureField("Password", text: $password)
                    .padding()
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                
                SecureField("Confirm Password", text: $confirmPassword)
                    .padding()
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                
                Button(action: {
                    createNewAdmin(username: username, password: password, confirmPassword: confirmPassword)
                }) {
                    Text("Create Admin")
                        .font(.title2)
                        .padding()
                        .background(Color.green)
                        .foregroundColor(.white)
                        .cornerRadius(8)
                }
                
                if !registrationStatusMessage.isEmpty {
                    Text(registrationStatusMessage)
                        .foregroundColor(.red)
                        .padding()
                }
                
                Spacer()
            }
            .padding()
        }
        
        // Function to handle new admin creation
        func createNewAdmin(username: String, password: String, confirmPassword: String) {
            guard !username.isEmpty, !password.isEmpty, !confirmPassword.isEmpty else {
                registrationStatusMessage = "Please fill out all fields."
                return
            }
            
            guard password == confirmPassword else {
                registrationStatusMessage = "Passwords do not match."
                return
            }
            
            let url = URL(string: "http://127.0.0.1:5000/admin/register_admin")!
            var request = URLRequest(url: url)
            request.httpMethod = "POST"
            request.setValue("application/json", forHTTPHeaderField: "Content-Type")
            
            let payload: [String: Any] = ["username": username, "password": password]
            
            do {
                request.httpBody = try JSONSerialization.data(withJSONObject: payload, options: [])
            } catch {
                registrationStatusMessage = "Error creating request: \(error.localizedDescription)"
                return
            }
            
            let task = URLSession.shared.dataTask(with: request) { data, response, error in
                if let error = error {
                    DispatchQueue.main.async {
                        self.registrationStatusMessage = "Registration failed: \(error.localizedDescription)"
                    }
                    return
                }
                
                guard let data = data else {
                    DispatchQueue.main.async {
                        self.registrationStatusMessage = "No data received."
                    }
                    return
                }
                
                do {
                    let responseJSON = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any]
                    if let message = responseJSON?["message"] as? String {
                        DispatchQueue.main.async {
                            self.registrationStatusMessage = message
                        }
                    }
                } catch {
                    DispatchQueue.main.async {
                        self.registrationStatusMessage = "Failed to parse response: \(error.localizedDescription)"
                    }
                }
            }
            
            task.resume()
        }
    }
    
    struct AdminDashboardView_Previews: PreviewProvider {
        static var previews: some View {
            AdminDashboardView()
        }
    }
    

