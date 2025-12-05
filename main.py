import asyncio
import os 
# Import the new utility file
from sensor_utils import get_environmental_data 

# 1. ADD IMPORTS FOR YOUR OTHER FILES HERE
from camera_utils import capture_leaf_image 
from gemini_analyzer import analyze_leaf_disease
from telegram_bot import send_telegram_message 

# 2. DEFINE CONFIGURATION VARIABLES HERE
TELEGRAM_BOT_TOKEN = "8570441603:AAFIdOR5hkE73JDbZZSm2vPlIQ0HaKjynfM" 
TELEGRAM_CHAT_ID = "6294416219" 
GEMINI_API_KEY = "AIzaSyCuuE6_I4NzmQz99ADo5a5sbb3wfND62Wk" 

# 3. DEFINE THE MAIN ASYNC FUNCTION FIRST
async def main_workflow():
    """Main function to run the capture, analysis, and notification process."""
    leaf_image_file = "current_leaf.jpg"
    
    # 1. Capture the image
    captured_path = capture_leaf_image(leaf_image_file)
    
    # 2. COLLECT ENVIRONMENTAL DATA (NEW STEP)
    environmental_data = get_environmental_data()
    print(f"Environmental Data Collected: {environmental_data}")
    
    if captured_path:
        # 3. Analyze the image with Gemini
        print("Sending image and environmental data to Gemini for analysis...")
        
        # ⚠️ MODIFIED CALL: PASSING THE GEMINI API KEY AND ENVIRONMENTAL DATA
        analysis_result = analyze_leaf_disease(
            captured_path, 
            GEMINI_API_KEY,
            environmental_data # <--- New argument added here
        )
        
        # 4. Send the image and result to Telegram
        print("Sending image and analysis to Telegram...")
        
        # The telegram_message text becomes the CAPTION
        caption_message = (
            "🌱 Analysis Report 🌱\n\n"
            f"{analysis_result}"
        )
        
        # 4a. FUNCTION CALL
        await send_telegram_message(
            captured_path, # ARGUMENT 1: The path to the image file
            caption_message, # ARGUMENT 2: The text that appears below the image
            TELEGRAM_BOT_TOKEN,
            TELEGRAM_CHAT_ID
        ) 
        
    else:
        # Fallback for camera error
        error_caption = "🚨 ERROR 🚨\n\nCould not capture image from USB camera."
        await send_telegram_message(
            "dummy_path.jpg",
            error_caption,
            TELEGRAM_BOT_TOKEN,
            TELEGRAM_CHAT_ID
        )

# 5. EXECUTE THE WORKFLOW
if __name__ == "__main__":
    print("Starting Leaf Analyzer Workflow...")
    asyncio.run(main_workflow())