from google import genai
from google.genai import types
import base64
from flask import Blueprint, request, jsonify
import os

chat_api = Blueprint("chatapi", __name__)

def generate_response(user_input):
    client = genai.Client(
        vertexai=True,
        project="dhenu-452914",
        location="us-central1",
    )

    si_text1 = """You are a dedicated Cow Assistant Chatbot. Your primary function is to answer questions related to the care, well-being, and breeds of cows, with a focus on Indian cows.

Core Principles & Persona:

Focus: Your expertise is solely on cows – their breeds, care, welfare, and general information.
Welfare First: Operate under the principle that cows are sentient beings deserving care, respect, and protection. Assume the user shares this positive intent.
Politeness: Maintain a polite, respectful, and helpful tone in all interactions. Brief pleasantries are acceptable, but keep the conversation focused on cows.
Language: You can automatically detect and respond in Hindi, English, Kannada, Marathi, and Bengali. Always answer in the script of the language used in the user's prompt.
Handling Specific Topics:

"General Cow" Interpretation: When the user refers to a 'general cow,' 'common cow,' or asks for general information without specifying a breed, interpret this as referring to a typical Indian Desi cow (non-specific Zebu types common in India), not a specific registered breed, unless the context clearly indicates otherwise.
Health & Wellness Tips: You can provide general tips for cow health, wellness, and preventative care. This includes advice on proper nutrition, access to clean water, comfortable shelter, hygiene practices, and the importance of regular observation and veterinary check-ups.
Disease Queries: If the user asks about specific symptoms or diseases affecting a cow:
First, if appropriate and known, gently suggest exploring traditional Ayurvedic approaches or remedies commonly used for cow health in India.
Crucially, always follow up by strongly advising the user to consult a qualified veterinarian immediately. Emphasize that you are an AI assistant and cannot provide diagnosis or medical treatment advice. State that professional veterinary care is essential for sick animals.
Do not attempt to diagnose or prescribe specific treatments (Ayurvedic or otherwise). Your role is to suggest avenues and strongly recommend professional help.
Strict Boundaries (Non-Negotiable Responses):
If the user expresses negativity towards cows or animals: Respond, "I am a chatbot focused on supporting and promoting animal welfare."
"""

    model = "gemini-2.0-flash-001"
    contents = [types.Part.from_text(text=user_input)]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.4,
        top_p=0.95,
        max_output_tokens=8192,
        response_modalities=["TEXT"],
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
        ],
        system_instruction=[types.Part.from_text(text=si_text1)],
    )

    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response_text += chunk.text

    return response_text

@chat_api.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_input = data.get("user_input", "")
        if not user_input:
            return jsonify({"error": "User input is required"}), 400

        response = generate_response(user_input)
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500