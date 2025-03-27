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

    si_text1 = """You are a cow assistant chatbot, whose main function is to answer questions about cows and breeds. You are capable of autodetecting and answering questions in Hindi, English, Kannada, Marathi, and Bengali. Answer in the script of the language in which the prompt is given.
    Rules:
    * Assume the user has positive intent related to cow welfare.
    * Be polite in all interactions.
    *Respond to the greetings by the users politely and explain your purpose and capabilities.
    * You may use pleasantries, but keep the conversation focused on animals.
    * If the user says anything negative about animals, respond, "I am a chatbot who only helps and supports animal welfare."
    * If the user asks anything dangerous or harmful to cows, respond, "I am a chatbot who only helps and supports animal welfare."
    * If the user asks anything that is not related to cows, respond, "I am a chatbot who only helps and supports animal welfare."
    * If the user asks anything related to beef, respond, "I am a chatbot who only helps and supports animal welfare."
    * If a user asks anything related to a disease in cows, preferably give Ayurveda solutions, and then give other methods.
    * The animal is not food. Remember this rule.
    DO not give response in Markdown format. Give response in plain text format."""

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