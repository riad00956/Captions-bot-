import logging
import random
from telegram import Update
from telegram.ext import (
Application,
CommandHandler,
MessageHandler,
ContextTypes,
filters
)

Enable logging

logging.basicConfig(
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
level=logging.INFO
)
logger = logging.getLogger(name)

Base templates for infinite caption generation

CAPTION_TEMPLATES = {
'en': {
'general': [
"Living my {adjective} life! {emoji}",
"{verb} {noun} like never before {emoji}",
"This {noun} deserves to be {verb} {emoji}",
"My {adjective} {noun} {verb} today {emoji}"
],
'nature': [
"{noun} never goes out of style {emoji}",
"The {nouns} are {verb} {emoji}",
"Lost in {adjective} {noun} {emoji}"
]
},
'bn': {
'general': [
"আমার {adjective} জীবন! {emoji}",
"{verb} {noun} আগের মতো না {emoji}",
"এই {noun} {verb} করার যোগ্য {emoji}",
"আজ আমার {adjective} {noun} {verb} {emoji}"
],
'nature': [
"{noun} স্টাইল হারায় না {emoji}",
"{nouns} {verb} করছে {emoji}",
"{adjective} {noun} এ হারিয়ে গেছি {emoji}"
]
}
}

Vocabulary for template filling

WORD_BANK = {
'en': {
'adjective': ['best', 'crazy', 'beautiful', 'wonderful', 'amazing'],
'noun': ['moment', 'day', 'time', 'life', 'adventure'],
'nouns': ['mountains', 'trees', 'waves', 'clouds'],
'verb': ['living', 'enjoying', 'remembering', 'loving', 'exploring'],
'emoji': ['🌟', '✨', '📸', '😊', '🌿']
},
'bn': {
'adjective': ['সেরা', 'পাগল', 'সুন্দর', 'চমৎকার', 'অসাধারণ'],
'noun': ['মুহূর্ত', 'দিন', 'সময়', 'জীবন', 'অ্যাডভেঞ্চার'],
'nouns': ['পাহাড়', 'গাছ', 'তরঙ্গ', 'মেঘ'],
'verb': ['যাপন', 'উপভোগ', 'মনে রাখা', 'ভালবাসা', 'অন্বেষণ'],
'emoji': ['🌟', '✨', '📸', '😊', '🌿']
}
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
"""Send welcome message."""
await update.message.reply_text(
"📸 Auto Caption Generator Bot\n\n"
"I can generate unlimited creative captions in:\n"
"- English 🇬🇧 (/language en)\n"
"- Bangla 🇧🇩 (/language bn)\n\n"
"Just send me a photo and I'll create unique captions every time!",
parse_mode='Markdown'
)
context.user_data['language'] = 'en'

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
"""Set language preference."""
if context.args and context.args[0].lower() in ['en', 'bn']:
language = context.args[0].lower()
context.user_data['language'] = language
await update.message.reply_text(
f"Language set to {'English' if language == 'en' else 'Bangla'}")
else:
await update.message.reply_text(
"Please specify:\n/language en\nor\n/language bn")

def generate_infinite_caption(language: str, category: str) -> str:
"""Generate unlimited unique captions using templates."""
template = random.choice(CAPTION_TEMPLATES[language][category])
words = WORD_BANK[language]

# Fill the template with random words  
caption = template.format(  
    adjective=random.choice(words['adjective']),  
    noun=random.choice(words['noun']),  
    nouns=random.choice(words['nouns']),  
    verb=random.choice(words['verb']),  
    emoji=random.choice(words['emoji'])  
)  
return caption

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
"""Generate unlimited captions for photos."""
try:
photo = update.message.photo[-1]
user_text = update.message.caption or ""
photo_type = detect_photo_type(user_text.lower())
language = context.user_data.get('language', 'en')

# Generate 3 unique caption options  
    captions = [  
        generate_infinite_caption(language, photo_type)  
        for _ in range(3)  
    ]  
      
    # Format response  
    response = (  
        f"📷 *Caption Options:*\n\n"  
        f"1️⃣ {captions[0]}\n"  
        f"2️⃣ {captions[1]}\n"  
        f"3️⃣ {captions[2]}\n\n"  
        f"Reply with 1-3 to select or send another photo for new options!"  
    )  
      
    # Send photo with first caption  
    await update.message.reply_photo(  
        photo=photo.file_id,  
        caption=captions[0],  
        reply_to_message_id=update.message.message_id  
    )  
      
    # Send caption options  
    await update.message.reply_text(  
        response,  
        parse_mode='Markdown',  
        reply_to_message_id=update.message.message_id  
    )  
      
except Exception as e:  
    logger.error(f"Error: {str(e)}")  
    await update.message.reply_text("Error generating captions. Please try again.")

def detect_photo_type(text: str) -> str:
"""Detect photo category."""
if any(word in text for word in ['nature', 'mountain', 'forest', 'tree']):
return 'nature'
return 'general'

def main():
TOKEN = '7412420290:AAHKHOBf1yuyiQjwk1V_0WPgxIAgtWNUH6c'  # Replace with your bot token

app = Application.builder().token(TOKEN).build()  
  
app.add_handler(CommandHandler("start", start))  
app.add_handler(CommandHandler("language", set_language))  
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))  
  
app.run_polling()

if name == 'main':
main()

