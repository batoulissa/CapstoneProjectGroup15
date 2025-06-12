# TheraTalk
Connecting patients and therapists with AI matching.



## 🌟 About TheraTalk
TheraTalk is a platform designed to help patients and therapists connect in an easier and faster way. It uses **AI-powered matching** to ensure optimal pairings based on individual needs and therapeutic approaches. Beyond matching, TheraTalk features an integrated **AI ChatBot**, powered by the **Gemini AI API**, offering instant support and guided conversations through advanced prompt training.

This platform was developed as a graduation project at Ewha Womans University, aiming to provide a seamless and effective solution for mental health access.



## ✨ Features
* **AI-Powered Therapist Matching:** Intelligent algorithms connect patients with the most suitable therapists.
* **Integrated AI ChatBot:** Offers instant support and guided conversations powered by Gemini AI.
* **Mood Log:** To help users reflect on their emotional patterns, we built a mood tracker. Users can select from emoticons to log how they feel every day.



## 🛠️ Technologies Used
* **Backend:** Python, Flask
* **Frontend:** JavaScript, CSS
* **AI:** The matching algorithm is built using Python, and the chatbot uses Google Gemini AI API.



## 🚀 Getting Started
To get TheraTalk up and running on your local machine, follow these steps:

### Prerequisites
Make sure that the following are installed in your environment:

#### Backend Environment:
* Python (3.8+)
* pip
* Conda (for environment management)

#### Frontend Environment:
* Node.js (14+)
* npm

### Installation
1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/batoulissa/CapstoneProjectGroup15.git](https://github.com/batoulissa/CapstoneProjectGroup15.git)
    cd CapstoneProjectGroup15
    ```

2.  **Backend Setup:**
    ```bash
    cd backend
    # It's highly recommended to use a virtual environment for Python projects
    conda create --name theratalk python=3.8 # Or your preferred Python version
    conda activate theratalk

    pip install -r requirements.txt
    
    # Set up your environment variables (e.g., Gemini AI API key). 
    ```

3.  **Frontend Setup:**
    ```bash
    cd ../frontend
    npm install
    ```



## ▶️ Running the Application
After following the installation steps, you can start the servers.

> **💡 Tip:** It's crucial to start the **backend server** before starting the **frontend server** for the application to function correctly.

1.  **Start Backend Server:**
    Navigate to the `backend` directory in your **activated Conda environment** (`conda activate theratalk`) and run:
    ```bash
    python3 app.py # Command to start the backend application
    ```
    The backend server will typically run on `http://127.0.0.1:5000` (or similar).

2.  **Start Frontend Server:**
    Open a *new* terminal window, navigate to the `frontend` directory, and run:
    ```bash
    npm start
    ```
    The frontend will typically open in your browser at `http://localhost:3000` (or similar).



## 💖 Our Team
TheraTalk was developed by a dedicated team as our graduation project:
* **Sanna Ascard-Soederstroem**: Backend Development, AI Development
* **Safarova Shohona**: UI/UX Design
* **Issa Batoul**: Frontend Development


