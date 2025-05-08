//
//  ContentView.swift
//  TheraTalk-Frontend
//
//  Created by Sanna on 2025-01-30.
//

import SwiftUI

struct ContentView: View {
    var body: some View {
        NavigationStack {
            VStack(spacing: 20) {
                Text("Welcome to TheraTalk!")
                    .font(.largeTitle)
                    .multilineTextAlignment(.center)
                    .padding()
                
                NavigationLink(destination: LoginView()) {
                    Text("Login")
                        .font(.title2)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color.orange)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                        .padding(.horizontal)
                }

                NavigationLink(destination: SignupView()) {
                    Text("Sign Up")
                        .font(.title2)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color.purple)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                        .padding(.horizontal)
                }

                NavigationLink(destination: ChatView()) {
                    Text("Go to Chat")
                        .font(.title2)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                        .padding(.horizontal)
                }

                NavigationLink(destination: ResourcesView()) {
                    Text("Mental Health Resources")
                        .font(.title2)
                        .padding()
                        .frame(maxWidth: .infinity)
                        .background(Color.green)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                        .padding(.horizontal)
                }
                NavigationLink(destination: AdminLoginView()) {
                    Text("Admin Login")
                        .font(.title3)
                        .foregroundColor(.blue)
                        .padding()
                        .background(Color.gray.opacity(0.2))
                        .cornerRadius(8)
                        .padding(.top)
                }
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
