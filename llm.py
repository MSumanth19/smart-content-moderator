import os
import google.generativeai as genai

# Configure the Gemini API client
genai.configure(api_key=os.environ.get("LLM_API_KEY"))

def moderate_text_content(text: str):
    """
    Sends text to the Gemini API for content classification.
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt = f"""
    Analyze the following text for inappropriate content and classify it as one of the following: toxic, spam, harassment, safe.
    Provide a confidence score from 0 to 100 and a brief reasoning for the classification.

    Text to analyze: "{text}"
    """
    try:
        response = model.generate_content(prompt)
        # You'll need to parse the response to get the JSON output.
        # This is a placeholder for the parsing logic.
        return {"classification": "safe", "confidence": 100, "reasoning": "Placeholder"}
    except Exception as e:
        print(f"LLM API error: {e}")
        return None

def moderate_image_content(image_data):
    """
    Sends image data to the Gemini Vision API for content classification.
    """
    # This function is called by the Celery worker
    model = genai.GenerativeModel('gemini-pro-vision')
    prompt = "Analyze the image for inappropriate content and classify it as toxic, spam, harassment, or safe."
    try:
        response = model.generate_content([prompt, image_data])
        return {"classification": "safe", "confidence": 100, "reasoning": "Placeholder"}
    except Exception as e:
        print(f"LLM API error: {e}")
        return None
