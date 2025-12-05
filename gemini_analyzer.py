from google import genai
from google.genai import types
import os

def analyze_leaf_disease(image_path, api_key, environmental_data): 
    """Sends the image and environmental data to Gemini for analysis."""
    
    # 1. Format the environmental data for the AI to understand
    # We keep the raw data here for easy insertion into the new section
    data_text = (
        f". Temperature: {environmental_data['temperature']}C\n"
        f". Humidity: {environmental_data['humidity']}%\n"
        f". Soil Moisture: {environmental_data['soil_moisture']}"
    )
    
    # 2. Define the prompt, including the data and strict formatting instructions
    prompt = (
        # Removed the environmental data from the analysis intro, as it's now a dedicated section.
        f"ANALYZE THIS IMAGE AND THE FOLLOWING ENVIRONMENTAL DATA. " 
        "Analyze the leaf image for disease or pests. Your response must be highly structured, "
        "professional, and concise, strictly following the format below. Respond in short, clear sentences."
        "Do NOT use emojis or long sentences, except for the section titles and the final closing line."
        "Use a period (.) followed by a space as the list marker (e.g., '. List item')." 
        
        # Instruction remains for the AI to cite the environmental data in the diagnosis
        "In the 'Likely Causes' section, specifically mention if the temperature or humidity contributed to the problem."

        "\n\n🎯 Diagnosis at a Glance"
        "\n State the primary disease or pest, with ONLY the disease name in capital (e.g., POWDERY MILDEW)."
        
        # NEW SECTION ADDED HERE: Environmental Context
        "\n\n🌡️ Current Environment" 
        f"\n. {data_text}" # Inserting the single line of environmental data here
        
        "\n\n🦠 Likely Causes"
        "\n. List 2-3 specific, concise environmental or pathogenic factors."
        
        "\n\n💉 Immediate Remedy"
        "\n. List 2-3 specific, clear, actionable treatment steps."
        
        "\n\n🛡️ Future Prevention"
        "\n. List 2-3 simple, clean tips for recurrence prevention."
        
        "\n\n🌱 "
        "\n Provide one short, motivational, and catchy phrase to end the report."
    )
    
    try:
        # 3. Initialize the client, passing the API key
        client = genai.Client(api_key=api_key)
        
        # 4. Load the image file directly into memory (as bytes) 
        if not os.path.exists(image_path):
             return f"Gemini API Error: Image file not found at {image_path}"
             
        with open(image_path, 'rb') as image_file:
            image_bytes = image_file.read()

        # Prepare the image file content using Part.from_bytes
        image_part = types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg")

        # 5. Call the API
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, image_part]
        )
        
        return response.text
        
    except Exception as e:
        # 6. Return a robust error message if the API call fails
        return f"Gemini API Error: {e}"