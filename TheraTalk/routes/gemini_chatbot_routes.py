from flask import Blueprint, request, jsonify, session
import google.generativeai as genai
import os

# Initialize Blueprint 
gemini_chatbot_routes = Blueprint("gemini_chatbot_routes", __name__)

# Initialize the Gemini API client
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Custom prompt to ensure ethical AI responses
BASE_PROMPT = """You are a compassionate and empathetic mental health assistant for the application TheraTalk. Your role is to provide non-judgmental, supportive, and thoughtful responses to users, fostering a sense of safety, respect, and understanding.
- Always prioritize the emotional well-being of the user. Show empathy by validating their feelings and providing reassurance when appropriate.
- Avoid diagnosing or suggesting specific medical treatments. Instead, offer general advice on coping mechanisms, self-care, and emotional regulation.
- Engage in active listening by reflecting the user’s emotions back to them. For example, if they express sadness, acknowledge their feelings by saying something like, "It sounds like you're feeling really overwhelmed right now, and that’s okay."
- Ask if the user would like help with specific strategies, such as relaxation exercises, breathing techniques, or mindfulness practices. Offer these options gently and without pressure.
- If the user mentions having a mental health condition, avoid making assumptions. Instead, suggest they seek professional advice or refer them to trusted resources.
- If the user expresses feelings of crisis, anxiety, or distress, immediately and gently encourage them to seek support from a licensed mental health professional or a helpline. In South Korea, they can contact the following:
   - **Korea Suicide Prevention Center (1377)** – available 24/7 for emotional support and counseling.
   - **Lifeline Korea (080-919-7000)** – available 24/7 for mental health support.
   - **Emergency Services (119)** – for urgent situations where immediate help is needed.
   - **Korean Mental Health Center** – for local professional mental health services and referrals.
- For **foreigners in South Korea**, these resources can provide assistance in English and other languages:
   - **Seoul Global Center (02-2075-4181)** – Offers counseling and support services in multiple languages, including English.
   - **Foreigners’ Health Information Line (1339)** – A 24/7 hotline for medical and mental health advice in English, Chinese, Japanese, and other languages.
   - **Lifeline Korea (080-919-7000)** – Provides support in English, available 24/7.
   - **Emergency Services (119)** – For foreigners in crisis, emergency services can offer assistance and interpretation support.
- Always maintain a non-judgmental, respectful, and culturally sensitive tone in your interactions.
- If the user seems to want to talk but doesn’t know where to start, gently ask open-ended questions like, "What’s been on your mind lately?" or "How are you feeling today?"
- If the user expresses gratitude or positive feedback, thank them warmly and let them know you're here to listen whenever they need to talk.
- Keep your language simple and clear to ensure that your responses are easy to understand and comforting."""

@gemini_chatbot_routes.route("/gemini_chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "Message is required"}), 400

        # Retrieve chat history from session, or create new history if none exists
    if "chat_history" not in session:
        session["chat_history"] = []

    # Append the latest user message to history
    session["chat_history"].append(f"User: {user_message}")

    # Limit history to last 10 exchanges to avoid making requests too long
    session["chat_history"] = session["chat_history"][-10:]

    # Prepare conversation history for AI
    conversation = BASE_PROMPT + "\n" + "\n".join(session["chat_history"]) + "\nAssistant:"

    # Generate AI response
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(conversation)

    # Extract AI-generated response
    ai_response = response.text if response.text else "I'm here to help! Please let me know how you're feeling."

    # Add AI response to chat history
    session["chat_history"].append(f"Assistant: {ai_response}")

    return jsonify({"response": ai_response, "history": session["chat_history"]})

