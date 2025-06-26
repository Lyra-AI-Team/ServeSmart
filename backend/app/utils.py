import os
from datetime import datetime
import numpy as np
import holidays as holidays_lib
from keras.models import load_model
from PIL import Image
from io import BytesIO
import base64
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.h5")
price_model = load_model(MODEL_PATH)

genai_api_key = os.getenv("API_KEY")
if genai_api_key:
    genai.configure(api_key=genai_api_key)

TR_HOLIDAYS = holidays_lib.Turkey()

# Ensure images directory exists
IMAGES_DIR = os.path.join(BASE_DIR, "product_images")
os.makedirs(IMAGES_DIR, exist_ok=True)

def calculate_discount() -> float:
    """Predict demand index and return discount percentage."""
    is_holiday = 1 if datetime.now().date() in TR_HOLIDAYS else 0
    hour = datetime.now().hour
    sin = np.sin(2 * np.pi * hour / 24)
    cos = np.cos(2 * np.pi * hour / 24)
    prediction = price_model.predict(np.array([[sin, cos, is_holiday]]))[0][0]

    if prediction > 2500:
        return 20.0
    elif prediction > 2000:
        return 10.0
    elif prediction > 1500:
        return 5.0
    return 0.0

def generate_title_description(exp: str) -> tuple[str, str]:
    """Use Gemini model to generate product title and description."""
    if not genai_api_key:
        raise RuntimeError("Google Generative AI API key not provided")

    model = genai.GenerativeModel("gemini-1.5-flash")
    prompt = f"""
You are extracting a food title and description from the given text, rewriting and enhancing the description when necessary.
Always respond in the user's input language.
Always answer in the given JSON format. Do not use any other keywords. Do not make up any information.
The description must contain at least 5 sentences.
JSON Format:
{{
"title": "<title of the food>",
"description": "<description of the food>"
}}
Examples:
Food Information: Rosehip Marmalade, keep it cold
Answer: {{"title": "Rosehip Marmalade", "description": "Store this delicious rose marmalade in a cold place. It's a wonderful flavor used in meals and desserts, sold in grocery stores. Packaged in 24g servings, it's a versatile addition to both meals and desserts!"}}
Food Information: Blackberry jam spoils in the heat
Answer: {{"title": "Blackberry Jam", "description": "Keep it in a cool place to preserve its sweetness. Best enjoyed at breakfast, this traditional flavor is available in markets and adds a unique touch to any meal."}}
Now answer this:
Food Information: {exp}
"""
    response = model.generate_content(prompt)
    import json
    parsed = json.loads(response.text)
    return parsed["title"], parsed["description"]

def save_image_from_upload(file_bytes: bytes, filename: str) -> str:
    """Save uploaded image bytes to disk and return path."""
    img = Image.open(BytesIO(file_bytes))
    path = os.path.join(IMAGES_DIR, filename)
    img.save(path)
    return path 