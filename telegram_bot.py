import os
import aiohttp 

# 🟢 CORRECT IMPORT: Get the necessary classes directly from the installed 'telegram' package
from telegram import Bot 
from telegram.helpers import escape_markdown

# 🛑 NOTE: Removed the incorrect line 'import telegram_bot'

# FUNCTION SIGNATURE MODIFIED: Now accepts image_path as the first argument
async def send_telegram_message(image_path: str, caption_message: str, token: str, chat_id: str):
    """
    Sends the image along with the analysis text as a caption to the specified Telegram chat.
    
    Args:
        image_path: Local path to the leaf image file.
        caption_message: The analysis text to be used as the caption.
        token: Your Telegram bot API token.
        chat_id: The recipient chat ID.
    """
    
    # 1. ESCAPE THE TEXT: This protects the caption from parsing errors when using MarkdownV2.
    # Note: escape_markdown is typically for text outside of markdown formatting. 
    # If your caption_message already contains intended markdown, you might need a different approach.
    # Assuming the content is plain text that needs escaping:
    escaped_caption_text = escape_markdown(caption_message, version=2) 
    
    # Check if the image file exists
    if not os.path.exists(image_path):
        # Fallback error message if the file is missing
        error_message = f"🚨 ERROR 🚨\n\nImage file not found at: `{image_path}`"
        
        # Send a plain text error message instead of failing completely
        try:
            # 🟢 CORRECT USAGE: Initialize Bot directly
            bot = Bot(token=token)
            await bot.send_message(chat_id=chat_id, text=error_message, parse_mode='MarkdownV2')
        except Exception as e:
            print(f"Telegram Bot Error during fallback: {e}")
        return

    try:
        # 🟢 CORRECT USAGE: Initialize Bot directly
        bot = Bot(token=token)
        
        # 2. SEND PHOTO: We use send_photo, and the text becomes the caption.
        # This requires the file to be opened in binary mode ('rb')
        with open(image_path, 'rb') as photo_file:
            await bot.send_photo(
                chat_id=chat_id, 
                photo=photo_file, 
                caption=escaped_caption_text, # The analysis is the caption
                parse_mode='MarkdownV2'      # Use MarkdownV2 for the caption
            )
        print("Image and analysis sent to Telegram successfully.")
        
    except Exception as e:
        print(f"Telegram Bot Error: {e}")