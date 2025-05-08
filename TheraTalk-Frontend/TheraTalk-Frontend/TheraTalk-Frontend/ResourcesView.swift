//
//  ResourcesView.swift
//  TheraTalk-Frontend
//
//  Created by Sanna on 2025-02-02.
//

import Foundation
import SwiftUI

struct ResourcesView: View {
    var body: some View {
        VStack {
            Text("Mental Health Resources")
                .font(.largeTitle)
                .padding()

            Text("📞 Crisis Hotline: 1-800-273-8255")
                .font(.title2)
                .padding()

            Text("🧘‍♂️ Meditation App: Headspace, Calm")
                .font(.title2)
                .padding()

            Text("📚 Therapy Resources: BetterHelp, Talkspace")
                .font(.title2)
                .padding()
        }
        .navigationTitle("Resources")
    }
}

struct ResourcesView_Previews: PreviewProvider {
    static var previews: some View {
        ResourcesView()
    }
}
