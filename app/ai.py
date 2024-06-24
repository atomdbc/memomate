import os
import ssl
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Set up Google Generative AI API key
genai.configure(api_key=os.getenv("GOOGLE_GEMINI"))
ssl._create_default_https_context = ssl._create_stdlib_context

# Set up text generation configuration
generation_config = {
    "temperature": 0.7,  # Lower temperature for more focused responses
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 150,  # Limit the length of the response
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.0-pro", generation_config=generation_config, safety_settings=safety_settings
)

async def generate_text(prompt):
    try:
        prompt_parts = [
            "You are a journaling assistant. Provide concise and direct responses to the user's journal entry. Do not give unsolicited advice.\n",
            "User: Today was a tough day. I felt overwhelmed with work.\n",
            "Assistant: What specifically made you feel overwhelmed today?\n",
            "User: I had a wonderful time with my family at the park. It was very refreshing.\n",
            "Assistant: What activities did you enjoy the most at the park?\n",
            f"User: {prompt}\n",
            "Assistant:"
        ]
        response = model.generate_content(prompt_parts)
        if response and response.candidates:
            return response.candidates[0].content.parts[0].text.strip()
        return "No response generated"
    except Exception as e:
        print(f"Error occurred during content generation: {e}")
        return "Error during generation"
