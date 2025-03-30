<!-- Template for PROJECT REPORT of Capstone Design 2025-2H, initially written by khyoo -->
<!-- This file is the basic template for the <1st Report> of the 2025 Computer Engineering Capstone Project. -->
<!-- The "*" symbols indicate italic formatting. -->
<!-- Please delete the "content" and fill in your team’s actual project details. -->

# Team Info
| (1) Project Title | *TheraTalk* |
|:---  |---  |
| (2) Team Number / Team Name | *15 - SSB* |
| (3) Team Members | ISSA BATOUL (2271098): Leader, Frontend <br> SAFAROVA SHOHONA (2271004): Member, *Frotend, UI Design* <br> ASCARD SOEDERSTROEM SANNA (2271001): Member, *Backend* |
| (4) Faculty Advisor | Professor 윤명국 |
| (5) Project Type | *산학* |
| (6) Project Keywords | *AI Therapy Matching, Mental Health App, Global Accessibility, Real-Time Chat, Auto Translation* |
| (7) Project Summary | *TheraTalk is an AI-powered mental health application designed to make therapy accessible anytime, anywhere for both international and Korean young adults. The app matches users with therapists based on preferences, specialties, and availability. It supports real-time chat therapy, guided self-help modules, and 24/7 AI chatbot support for instant mental health guidance. A key feature is auto-translation, allowing users to connect with global therapists even during off-hours. Users can track their mood, receive personalized mental health tips, and access therapist profiles with scheduling and reviews. The app also includes a community forum and psychology-based quizzes for self-discovery and connection. Designed for mobile accessibility and privacy, TheraTalk bridges global mental health support with AI-powered convenience* |

<br>

# Project Summary
| Item | Content |
|:---  |---  |
| (1) Problem Definition | *Many young adults face limited access to mental health support due to language barriers, time zones, and availability—especially in South Korea where therapy is often stigmatized or inaccessible. Our target users are international and Korean young adults who need flexible and culturally relevant therapy options.* |
| (2) Comparison with Existing Research | *Apps like BetterHelp and Labayh offer online therapy but lack global accessibility, real-time matching, and multilingual features. TheraTalk improves on these by offering AI matching, auto-translation, and 24/7 chat access, making therapy more inclusive and available.* |
| (3) Proposed Solution | *TheraTalk is a mental health app powered by Google Gemini AI that connects users with therapists based on preferences, language, and availability. Key features include: -24/7 chat therapy -AI chatbot support -Auto-translation for global therapist access -Self-help modules and mood tracking* |
| (4) Expected Impact and Significance | *TheraTalk helps normalize and improve access to therapy across borders. It offers convenient, on-demand, and inclusive mental health support, especially for young people who might not seek traditional therapy.* |
| (5) List of Core Features | *List of Core Features: 1.Language Option – Multilingual interface and language toggle 2.Appointment Booking – Book and manage therapist sessions 3.Payment Options – KakaoPay, PayPal, subscription or per session 4.Chat-Based Therapy – Real-time secure chat (Flask + SocketIO) 5.AI Matching Algorithm – Matches based on user preferences 6.AI Chatbot – Instant 24/7 support and crisis help 7.Self-Help Modules – Educational content and exercises 8.Mood Tracking – Daily logs, analytics, and sharing with therapist 9.Affirmations & Tips – Personalized daily wellness tips 10.Therapist Profiles – Info, ratings, availability 11.Chat Notifications – Real-time message alertsm 12.Community Forums – Peer support in anonymous, safe spaces 13.Mental Health Quizzes – Assessments with shareable results 14.Video Courses – Self-paced therapy content* |

<br>

# Project Design & Implementation
| Item | Content |
|:---  |---  |
| (1) Requirements Specification | *We use a combination of methods to specify requirements: Use Case Descriptions for user interaction flows (e.g., booking, chatting, mood tracking) UI Wireframes and Prototypes created by the design team to define user experience Class and Module Specs for backend logic (matching, payment, chat, etc.) E-R Diagram to define relationships between users, therapists, sessions, and chats* <br> Examples: <br> - Detailed requirements per function (or use cases) <br> - Design models (class diagrams, class/module specs) <br> - UI analysis/design models <br> - E-R diagram / DB design model (table structure) |
| (2) Overall System Architecture | *TheraTalk follows a client-server model with a mobile frontend and Flask-based backend. Frontend (React Native): Handles user interface, multilingual support, mood tracking, and chat Backend (Flask, Python): Manages user data, chat system (via SocketIO), booking, and AI matching Database (PostgreSQL): Stores users, therapist data, schedules, and message history AI Services: Google Gemini AI for chatbot, OpenAI API for sentiment analysis Third-party Modules: KakaoPay & PayPal APIs (payments) SocketIO (real-time chat) Translation API (auto-translation)* |
| (3) Core Engine and Feature Design | *Matching Engine: Takes user input (language, preferences, mental health goals) and returns best-fit therapists using weighted scoring. Chat Engine: Real-time communication using SocketIO with secure message logging and multilingual interface support. AI Chatbot Engine: Uses Gemini AI to provide 24/7 responses; handles basic emotional support and suggests resources based on sentiment detection. Auto-Translation Engine: Middleware detects message language and translates in real-time between patient and therapist using external translation APIs.* |
| (4) Implementation of Key Features | *1. Therapist Matching Algorithm -User answers onboarding questions about language, therapy goals, availability -The system uses a scoring algorithm to compare with therapist attributes -Backend returns a ranked list of therapists via REST API -Frontend displays profiles with filters for user refinement 2. Chat-Based Therapy with Auto-Translation -Flask + SocketIO handles real-time messaging -Each message is passed through the translation API if patient and therapist languages differ -Messages are stored in the database with timestamps and language metadata -The frontend displays translated and original versions for transparency.* |
| (5) Other | *Add any other relevant information.* | 
![TheraTalk System Architecture](theratalk-diagram.png)



<br>
