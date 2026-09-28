import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import pyotp
from urllib.parse import urlparse, parse_qs

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = (
        "Hello! 👋\n"
        "Mujhe apna `otpauth://` URL bhejiye, aur main aapko uska current live TOTP code generate karke dunga."
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown")

# Message handler (URL process karne ke liye)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    # Check karein ki text otpauth se start hota hai ya nahi
    if text.startswith("otpauth://"):
        try:
        # OTPAuth URL se secret key extract karna
            parsed_url = urlparse(text)
            query_params = parse_qs(parsed_url.query)
            
            if 'secret' not in query_params:
                await update.message.reply_text("❌ Error: Diye gaye URL mein secret key nahi mili.")
                return
                
            secret = query_params['secret'][0]
            
            # Pyotp ke zariye live TOTP code generate karna
            totp = pyotp.TOTP(secret)
            current_code = totp.now()
            
            # User ko code bhejna
            response = (
                f"✅ **Live OTP Code:** `{current_code}`\n\n"
                f"*(Note: Yeh code kuch hi seconds mein expire ho jayega)*"
            )
            await update.message.reply_text(response, parse_mode="Markdown")
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error: URL parse karne mein samasya aayi. Kripya sahi URL bhejiye.")
    else:
        await update.message.reply_text("⚠️ Kripya valid `otpauth://` URL hi bhejiye.")

def main():
    # Apna Telegram Bot Token yahan daalein
    TOKEN = "8857943016:AAEZp1cMhRHj0aafORKQ3OXTvXdvZesUXeQ"
    
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Handlers register karein
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Bot is running...")
    application.run_polling()

if __name__ == '__main__':
    main()
