//
//  TherapistDashboardView.swift
//  TheraTalk-Frontend
//
//  Created by Sanna on 2025-02-02.
//

import Foundation
import SwiftUI

struct TherapistDashboardView: View {
    var body: some View {
        VStack {
            Text("Therapist Dashboard")
                .font(.largeTitle)
                .padding()

            Text("Welcome, Therapist! View patient messages, schedule appointments, and provide support.")
                .padding()
        }
    }
}

struct TherapistDashboardView_Previews: PreviewProvider {
    static var previews: some View {
        TherapistDashboardView()
    }
}
