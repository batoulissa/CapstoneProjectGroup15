//
//  SignUpView.swift
//  TheraTalk-Frontend
//
//  Created by Sanna on 2025-02-02.
//

import Foundation
import SwiftUI

struct SignupView: View {
    @State private var name: String = ""
    @State private var age: String = ""
    @State private var gender: String = ""
    @State private var medicalHistory: String = ""
    @State private var therapyNeed: String = ""
    @State private var languages: String = ""
    @State private var availability: String = ""
    @State private var password: String = ""
    @State private var confirmPassword: String = ""
    @State private var selectedRole: String = "Patient"  // Default role
    @State private var showError: Bool = false
    @State private var errorMessage: String = ""
    
    @State private var fileUrl: URL?  // For file uploads
    @State private var isImagePickerPresented: Bool = false

    let roles = ["Patient", "Therapist"]

    var body: some View {
        VStack {
            Text("Sign Up")
                .font(.largeTitle)
                .padding()

            TextField("Name", text: $name)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()

            if selectedRole == "Patient" {
                TextField("Age", text: $age)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()

                TextField("Gender", text: $gender)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()

                TextField("Medical History", text: $medicalHistory)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()

                TextField("Therapy Need", text: $therapyNeed)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()

                TextField("Languages", text: $languages)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()

                TextField("Availability", text: $availability)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()
            } else if selectedRole == "Therapist" {
                TextField("Experience Years", text: $age)  // Reusing 'age' field for years of experience
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()

                TextField("Languages", text: $languages)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()

                TextField("Focus Areas", text: $therapyNeed)  // Reusing 'therapyNeed' field for focus areas
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .padding()
            }

            SecureField("Password", text: $password)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()

            SecureField("Confirm Password", text: $confirmPassword)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .padding()

            Picker("Select Role", selection: $selectedRole) {
                ForEach(roles, id: \.self) { role in
                    Text(role)
                }
            }
            .pickerStyle(SegmentedPickerStyle())
            .padding()

            Button(action: {
                if name.isEmpty || password.isEmpty || confirmPassword.isEmpty {
                    showError = true
                    errorMessage = "⚠️ Please fill in all fields"
                } else if password != confirmPassword {
                    showError = true
                    errorMessage = "⚠️ Passwords do not match"
                } else {
                    signUpUser()
                }
            }) {
                Text("Sign Up")
                    .font(.title2)
                    .padding()
                    .frame(maxWidth: .infinity)
                    .background(Color.purple)
                    .foregroundColor(.white)
                    .cornerRadius(10)
                    .padding(.horizontal)
            }

            if showError {
                Text(errorMessage)
                    .foregroundColor(.red)
                    .padding()
            }

            // File Picker Button
            Button("Upload Identification/Proof of Education") {
                isImagePickerPresented.toggle()
            }
            .padding()

        }
        .navigationTitle("Sign Up")
        .fileImporter(isPresented: $isImagePickerPresented, allowedContentTypes: [.pdf]) { result in
            do {
                let selectedFile: URL = try result.get()
                fileUrl = selectedFile
            } catch {
                errorMessage = "⚠️ Failed to select file"
                showError = true
            }
        }
    }

    func signUpUser() {
        var urlString: String
        if selectedRole == "Patient" {
            urlString = "http://127.0.0.1:5000/patient/register"
        } else {
            urlString = "http://127.0.0.1:5000/therapist/register"
        }

        guard let url = URL(string: urlString) else { return }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        
        var body = [
            "name": name,
            "password": password,
            "age": age,
            "gender": gender,
            "medical_history": medicalHistory,
            "therapy_need": therapyNeed,
            "languages": languages,
            "availability": availability
        ]

        if let fileUrl = fileUrl {
            body["file"] = fileUrl.absoluteString  // Add file URL to body for backend processing
        }

        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: body)
        } catch {
            errorMessage = "⚠️ Failed to create request"
            showError = true
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
            if let responseJSON = try? JSONDecoder().decode(SignupResponse.self, from: data) {
                DispatchQueue.main.async {
                    if responseJSON.message == "Patient registered successfully!" || responseJSON.message == "Therapist registration is pending approval!" {
                        // Handle success, maybe navigate to login screen or welcome
                        print("Registration successful!")
                    } else {
                        showError = true
                        errorMessage = responseJSON.message
                    }
                }
            } else {
                DispatchQueue.main.async {
                    showError = true
                    errorMessage = "⚠️ Unexpected response from server"
                }
            }
        }
        task.resume()
    }
}

struct SignupResponse: Codable {
    let message: String
}

struct SignupView_Previews: PreviewProvider {
    static var previews: some View {
        SignupView()
    }
}
