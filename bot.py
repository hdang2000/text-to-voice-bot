import os
from telegram import Update
from telegram.ext import CommandHandler
from telegram import InputFile
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from gtts import gTTS

BOT_TOKEN = os.environ["BOT_TOKEN"]

# Ensure a folder exists to store voice files temporarily
os.makedirs("voice_temp", exist_ok=True)

async def text_to_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.message.from_user.id
    audio_path = f"voice_temp/voice_{user_id}.mp3"

    # Convert text to voice
    tts = gTTS(text=user_text)
    tts.save(audio_path)

    # Send the voice note back
    with open(audio_path, "rb") as audio:
        print(f"Sending voice file: {audio_path}")
        await update.message.reply_voice(voice=InputFile(audio))


    os.remove(audio_path)  # Clean up after sending

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Welcome to the Dang's - Text-to-Voice Bot!*\n\n"
        "Just send me any text message, and I'll convert it into a voice note 🎙️\n\n"
        "You can send the message in either English or Hindi\n\n"
        "_Try sending a message now!_",
        parse_mode="Markdown"
    )

async def error_handler(update, context):
    print(f"Update: {update}")
    print(f"Error: {context.error}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), text_to_voice))
    print("Bot is running...")
    app.run_polling()