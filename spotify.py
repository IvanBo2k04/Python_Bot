import os
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import socket

# Получаем ключи доступа к API Spotify
client_id = os.environ.get('a3b675af734a4888ad8988fb8340f830')
client_secret = os.environ.get('664935e1879348629a9cf9f07cdbe205')
redirect_uri = os.environ.get('http://localhost:8000/callback')

# Инициализируем Spotipy и получаем доступ к аккаунту Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='a3b675af734a4888ad8988fb8340f830',
    client_secret='664935e1879348629a9cf9f07cdbe205',
    redirect_uri='http://localhost:8000/callback',
    scope='playlist-modify-public'
))

# Обработчик команды /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот для поиска и добавления треков в плейлист на Spotify. Чтобы начать, просто отправь мне название трека или исполнителя.")

# Обработчик текстовых сообщений
def text(update, context):
    # Получаем текст сообщения
    query = update.message.text
    # Ищем треки на Spotify
    results = sp.search(q=query, limit=10)
    # Получаем первый найденный трек
    if len(results['tracks']['items']) > 0:
        track = results['tracks']['items'][0]
        # Получаем название трека и исполнителя
        track_name = track['name']
        artist_name = track['artists'][0]['name']
        # Получаем идентификатор публичного плейлиста
        playlist_id = '2feyZP0GrTZDfgB6cDYCBQ'
        # Добавляем трек в плейлист
        sp.user_playlist_add_tracks(user='IvanBo2k04', playlist_id=playlist_id, tracks=[track['uri']])
        # Отправляем сообщение пользователю с подтверждением добавления трека
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Трек \"{track_name}\" исполнителя {artist_name} был успешно добавлен в плейлист!")
    else:
        # Если трек не найден, отправляем случайное сообщение
        messages = ["К сожалению, я не нашел такой трек. Попробуйте еще раз.", "Мне не удалось найти этот трек. Попробуйте другой запрос."]
        context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(messages))

# Инициализируем бота и добавляем обработчики команд и сообщений
updater = Updater(token='6197462837:AAEQGmz1tCvZIxSht75qaXGamfxA_jb3_gY', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text))

# Запускаем бота
updater.start_polling()
updater.idle()
