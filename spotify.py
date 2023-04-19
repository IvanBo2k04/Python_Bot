import os
import random
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import socket
import time
import logging

client_id = os.environ.get('a3b675af734a4888ad8988fb8340f830')
client_secret = os.environ.get('513934604d22405d80d28e2dae064bcc')
redirect_uri = os.environ.get('http://localhost:8000/callback')

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id='a3b675af734a4888ad8988fb8340f830',
    client_secret='513934604d22405d80d28e2dae064bcc',
    redirect_uri='http://localhost:8000/callback',
    scope='playlist-modify-public'
))

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот для поиска и добавления треков в плейлист на Spotify. Чтобы начать, просто отправь мне название трека или исполнителя.")

try:
    def text(update, context):
        query = update.message.text
        results = sp.search(q=query, limit=10)
        time.sleep(4)  # добавляем задержку в 2 секунды
        if len(results['tracks']['items']) > 0:
            track = results['tracks']['items'][0]
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            playlist_id = '2feyZP0GrTZDfgB6cDYCBQ'
            sp.user_playlist_add_tracks(user='31lbtl3dfbxe5hffhfhcjg2zfn3y', playlist_id=playlist_id, tracks=[track['uri']])
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Трек \"{track_name}\" исполнителя {artist_name} был успешно добавлен в плейлист!")
        else:
            messages = ["К сожалению, я не нашел такой трек. Попробуйте еще раз.", "Мне не удалось найти этот трек. Попробуйте другой запрос."]
            context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(messages))
except Exception as e:
    logging.exception("Exception occurred: {}".format(e))

updater = Updater(token='6197462837:AAEQGmz1tCvZIxSht75qaXGamfxA_jb3_gY', use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, text))

updater.start_polling()
updater.idle()
