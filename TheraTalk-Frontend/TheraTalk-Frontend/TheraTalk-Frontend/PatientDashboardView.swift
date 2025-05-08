//
//  PatientDashboardView.swift
//  TheraTalk-Frontend
//
//  Created by Sanna on 2025-02-02.
//

import Foundation
import SwiftUI

struct PatientDashboardView: View {
    var body: some View {
        VStack {
            Text("Patient Dashboard")
                .font(.largeTitle)
                .padding()

            Text("Welcome! Here you can chat with a therapist, view resources, and track your progress.")
                .padding()
        }
    }
}

struct PatientDashboardView_Previews: PreviewProvider {
    static var previews: some View {
        PatientDashboardView()
    }
}
