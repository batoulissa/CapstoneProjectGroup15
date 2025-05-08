//
//  ChatView.swift
//  TheraTalk-Frontend
//
//  Created by Sanna on 2025-02-02.
//

import Foundation
import SwiftUI

struct ChatMessage: Identifiable {
    let id = UUID()
    let text: String
    let isUser: Bool
}

struct ChatView: View {
    @State private var messages: [ChatMessage] = []
    @State private var userInput: String = ""

    var body: some View {
        VStack {
            List(messages) { message in
                HStack {
                    if message.isUser {
                        Spacer()
                        Text(message.text)
                            .padding()
                            .background(Color.blue.opacity(0.7))
                            .foregroundColor(.white)
                            .cornerRadius(10)
                            .frame(maxWidth: 250, alignment: .trailing)
                    } else {
                        Text(message.text)
                            .padding()
                            .background(Color.gray.opacity(0.2))
                            .cornerRadius(10)
                            .frame(maxWidth: 250, alignment: .leading)
                        Spacer()
                    }
                }
            }
            
            HStack {
                TextField("Type a message...", text: $userInput)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
                    .frame(minHeight: 40)

                Button(action: sendMessage) {
                    Image(systemName: "paperplane.fill")
                        .foregroundColor(.white)
                        .padding()
                        .background(Color.blue)
                        .clipShape(Circle())
                }
            }
            .padding()
        }
        .navigationTitle("Chatbot")
    }

    func sendMessage() {
        guard !userInput.trimmingCharacters(in: .whitespaces).isEmpty else { return }

        let userMessage = ChatMessage(text: userInput, isUser: true)
        messages.append(userMessage)

        sendMessageToChatbot(message: userInput) { responseText in
            DispatchQueue.main.async {
                let botMessage = ChatMessage(text: responseText, isUser: false)
                messages.append(botMessage)
            }
        }

        userInput = ""
    }

    func sendMessageToChatbot(message: String, completion: @escaping (String) -> Void) {
        let url = URL(string: "http://127.0.0.1:5000/chatbot/chat")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let payload: [String: Any] = ["message": message]

        do {
            request.httpBody = try JSONSerialization.data(withJSONObject: payload, options: [])
        } catch {
            print("❌ Error serializing message to JSON: \(error)")
            return
        }

        let task = URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("❌ Request Error: \(error.localizedDescription)")
                return
            }

            guard let data = data else { return }

            do {
                let jsonResponse = try JSONSerialization.jsonObject(with: data, options: []) as? [String: Any]
                if let responseText = jsonResponse?["response"] as? String {
                    completion(responseText)
                }
            } catch {
                print("❌ Failed to parse JSON response: \(error.localizedDescription)")
            }
        }
        task.resume()
    }
}
