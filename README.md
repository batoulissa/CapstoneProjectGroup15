# TheraTalk

TheraTalk is a mental health therapy app that connects patients and doctors, inspired by platforms like Labayh. This project includes a frontend built with React Native and a backend built with Python using Flask.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
  - [Frontend](#frontend): MyFirstApp
  - [Backend](#backend): TheraTalk
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Features

- User authentication for patients and doctors.
- Mood tracking with selectable emotions.
- Book and manage 1-on-1 therapy sessions.
- Access to a journal and library for mental wellness resources.
- Notification system for reminders and updates.

## Technologies Used

### Frontend (MyFirstApp)
- React Native
- Expo

### Backend (TheraTalk)
- Python
- Flask
- Flask-SQLAlchemy
- Flask-CORS

## Setup Instructions

### Frontend
1. Navigate to the `frontend` folder.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```
4. Scan the QR code to launch the app on your device (via Expo Go) or in an emulator.

### Backend
1. Navigate to the `backend` folder.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv environment
   source environment/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Flask server:
   ```bash
   python app.py
   ```

### Notes
- Ensure both frontend and backend are running to see full functionality.
- Update API URLs in the frontend to match the backend's IP address and port.


## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
