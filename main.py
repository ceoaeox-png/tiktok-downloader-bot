import telebot
import requests
import os

# ТВОЙ ТОКЕН ИЗ BOTFATHER
TOKEN = '8770213821:AAEwQhheszIwtkp3cxCHwHIUcJYexPbfzQA'
bot = telebot.TeleBot(TOKEN)

def get_tiktok_data(url):
    # Используем открытое API для получения прямых ссылок
    api_url = f"https://www.tikwm.com/api/?url={url}"
    response = requests.get(api_url).json()
    
    if response.get('code') == 0:
        data = response['data']
        return {
            'video': data['play'],      # Видео без водяного знака
            'audio': data['music'],     # Прямая ссылка на MP3
            'title': data.get('title', 'video')
        }
    return None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Пришли ссылку на TikTok. Я пришлю видео без водяного знака и музыку!")

@bot.message_handler(func=lambda m: 'tiktok.com' in m.text)
def handle_tiktok(message):
    status = bot.reply_to(message, "⏳ Обрабатываю ссылку...")
    
    try:
        data = get_tiktok_data(message.text)
        
        if data:
            # Отправляем видео
            bot.send_video(message.chat.id, data['video'], caption="🎬 Видео без водяного знака")
            
            # Отправляем аудио
            bot.send_audio(message.chat.id, data['audio'], caption="🎵 Музыка из видео")
            
            bot.delete_message(message.chat.id, status.message_id)
        else:
            bot.edit_message_text("❌ Не удалось получить данные. Проверь ссылку.", message.chat.id, status.message_id)
            
    except Exception as e:
        bot.edit_message_text(f"⚠️ Ошибка: {str(e)}", message.chat.id, status.message_id)

if __name__ == "__main__":
    print("Бот через API запущен!")
    bot.infinity_polling()
  
