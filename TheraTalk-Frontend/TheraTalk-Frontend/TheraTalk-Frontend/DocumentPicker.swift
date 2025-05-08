//
//  DocumentPicker.swift
//  TheraTalk-Frontend
//
//  Created by Sanna on 2025-02-02.
//

import SwiftUI
import MobileCoreServices

// 1. Create a Document Picker
struct DocumentPicker: UIViewControllerRepresentable {
    class Coordinator: NSObject, UIDocumentPickerDelegate {
        var parent: DocumentPicker
        
        init(parent: DocumentPicker) {
            self.parent = parent
        }
        
        func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentsAt urls: [URL]) {
            parent.didPickFile(urls.first)  // Here no argument label
        }
        
        func documentPickerWasCancelled(_ controller: UIDocumentPickerViewController) {
            parent.didCancel()
        }
    }
    
    var didPickFile: (URL?) -> Void
    var didCancel: () -> Void
    
    func makeCoordinator() -> Coordinator {
        return Coordinator(parent: self)
    }
    
    func makeUIViewController(context: Context) -> UIDocumentPickerViewController {
        let documentPicker = UIDocumentPickerViewController(forOpeningContentTypes: [.pdf], asCopy: true)
        documentPicker.delegate = context.coordinator
        return documentPicker
    }
    
    func updateUIViewController(_ uiViewController: UIDocumentPickerViewController, context: Context) {
        // No need to update the controller
    }
}
