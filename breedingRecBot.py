from google import genai
from google.genai import types
from flask import Blueprint, request, jsonify

breeding_rec_api = Blueprint("breeding_rec_api", __name__)

def generate_breeding_recommendation(breed):
    client = genai.Client(
        vertexai=True,
        project="dhenu-452914",
        location="us-central1",
    )

    si_text1 = f"""You are an expert in Indian cow breeding. The selected cow breed is *{breed}*.
Generate a Markdown table with four columns and a header row. The columns should be titled:
\"Feature | Selected Breed | Recommended Crossbreed | Reason for Crossbreeding\"

Please generate three rows corresponding to the following features:
1. *Higher Milk Production:* Increase milk yield while maintaining resilience.
2. *Better Heat & Disease Resistance:* Improve adaptability in tropical climates.
3. *Higher Butterfat Content:* Enhance milk quality for dairy products such as ghee.

For each row:
- Column \"Feature\" lists the feature name.
- Column \"Selected Breed\" displays the breed provided (i.e., *{breed}*).
- Column \"Recommended Crossbreed\" suggests an Indian cow breed for crossbreeding.
- Column \"Reason for Crossbreeding\" explains why that crossbreed is recommended.

The table should include three rows corresponding to the fixed features:
1. Higher Milk Production
2. Better Heat & Disease Resistance
3. Higher Butterfat Content

Give me output in JSON format."""

    model = "gemini-2.0-flash-001"
    contents = [types.Part.from_text(text="Generate breeding recommendations")]
    tools = [
        types.Tool(google_search=types.GoogleSearch()),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=0.7,
        top_p=0.95,
        max_output_tokens=8192,
        response_modalities=["TEXT"],
        safety_settings=[
            types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="OFF"),
            types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="OFF"),
        ],
        tools=tools,
        system_instruction=[types.Part.from_text(text=si_text1)],
    )

    response_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
            continue
        response_text += chunk.text

    return response_text

@breeding_rec_api.route('/breeding_recommendation', methods=['POST'])
def breeding_recommendation():
    try:
        data = request.json
        breed = data.get("breed", "")
        if not breed:
            return jsonify({"error": "Breed is required"}), 400

        response = generate_breeding_recommendation(breed)
        return jsonify({"recommendation": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500