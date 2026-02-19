import os
import logging
import asyncio
from telegram import Update, InputMediaPhoto, InputMediaVideo
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from app.config import Config
from app.downloader import InstagramDownloader
from app.security import rate_limiter, is_admin
from app.utils import is_instagram_url

# Initialize logging
logger = logging.getLogger(__name__)

# Initialize Downloader
downloader = InstagramDownloader()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 ¡Hola! Soy el Bot de Descarga de Instagram.\n\n"
        "Envíame un enlace de Instagram y descargaré el contenido por ti.\n"
        "Usa /help para ver más información."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 **Instrucciones:**\n\n"
        "1. Copia el enlace de un post, reel o video de Instagram.\n"
        "2. Pégalo aquí en el chat.\n"
        "3. Espera a que descargue y te lo envíe.\n\n"
        "⚠️ _Nota: Solo puedo descargar contenido de cuentas públicas o de cuentas que sigo._"
    , parse_mode='Markdown')

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return # Ignore non-admins
    
    await update.message.reply_text(
        f"✅ **Estado del Bot**\n"
        f"Instagram Logged In: {'Sí' if downloader.logged_in else 'No'}\n"
        f"Admin ID: {Config.ADMIN_TELEGRAM_ID}"
    , parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if not is_instagram_url(text):
        await update.message.reply_text("❌ Enlace no válido. Por favor envía un enlace de Instagram.")
        return

    # Rate Limiting
    if not is_admin(user_id) and not rate_limiter.is_allowed(user_id):
        await update.message.reply_text("⏳ Estás enviando muchas solicitudes. Por favor espera un momento.")
        return

    status_msg = await update.message.reply_text("📥 Descargando contenido...")
    download_path = None

    try:
        # Run synchronous Instaloader code in a separate thread to avoid blocking the bot
        loop = asyncio.get_running_loop()
        media_files, path = await loop.run_in_executor(None, downloader.download_post, text)
        download_path = path

        if not media_files:
            await status_msg.edit_text("❌ No se encontró contenido multimedia para descargar.")
            return

        await status_msg.edit_text("📤 Subiendo a Telegram...")

        # Send files
        if len(media_files) == 1:
            file_path = media_files[0]
            if file_path.endswith('.mp4'):
                await update.message.reply_video(video=open(file_path, 'rb'))
            else:
                await update.message.reply_photo(photo=open(file_path, 'rb'))
        else:
            # Send as album
            media_group = []
            for file_path in media_files:
                if file_path.endswith('.mp4'):
                    media_group.append(InputMediaVideo(open(file_path, 'rb')))
                else:
                    media_group.append(InputMediaPhoto(open(file_path, 'rb')))
            
            # Telegram allows max 10 items per media group
            # Chunking if necessary (simple implementation for now usually < 10)
            if len(media_group) > 10:
                await update.message.reply_text("⚠️ El post tiene más de 10 archivos. Enviando los primeros 10.")
                media_group = media_group[:10]
            
            await update.message.reply_media_group(media=media_group)

        await status_msg.edit_text("✅ Descarga completada.")

    except Exception as e:
        logger.error(f"Error processing URL {text}: {e}")
        await status_msg.edit_text(f"❌ Error al descargar: {str(e)}")
    
    finally:
        # Cleanup
        if download_path:
            downloader.cleanup(download_path)

def main():
    Config.validate()
    
    application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Webhook setup
    webhook_url = f"https://{Config.DOMAIN}/{Config.TELEGRAM_BOT_TOKEN}"
    logger.info(f"Starting webhook on {webhook_url} port {Config.PORT}")
    
    application.run_webhook(
        listen="0.0.0.0",
        port=Config.PORT,
        url_path=Config.TELEGRAM_BOT_TOKEN,
        webhook_url=webhook_url,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    main()
