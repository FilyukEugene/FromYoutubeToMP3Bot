from pytube import YouTube
from moviepy.editor import *
import telebot
import os

bot = telebot.TeleBot('6081563935:AAH_KlCGMZCvgf_hgScUwcC4hEl2QCf3eSc')


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Привіт, <b>{message.from_user.first_name} {message.from_user.last_name}</b>',
                     parse_mode='html')
    bot.send_message(message.chat.id, '<b>Використай меню</b>',
                     parse_mode='html')


@bot.message_handler(commands=['help'])
def help_information(message):
    bot.send_message(message.chat.id, '<b>Телеграм бот для завантажування '
                                      'mp3 файлів із відео ютуб використовуючи посилання</b>',
                     parse_mode='html')


@bot.message_handler()
def send_audio(message):
    bot.send_message(message.chat.id, 'Зачекай поки бот виконає деякі операції...')
    youtube_object = YouTube(message.text)
    youtube_object = youtube_object.streams.get_highest_resolution()
    try:
        youtube_object.download()
        mp4_path = youtube_object.default_filename
        audio_name = youtube_object.default_filename.replace('mp4', '')
        audio_name = "".join(ch.lower() for ch in audio_name if ch.isalnum())

        with VideoFileClip(mp4_path) as video:
            audio_path = f'{audio_name}.mp3'
            video.audio.write_audiofile(audio_path)

            bot.reply_to(message, "Ось твоя музика -->")
            bot.send_audio(message.chat.id, audio=open(audio_path, 'rb'))

        if os.path.exists(audio_path):
            os.remove(audio_path)
            print(f"{audio_path} deleted successfully.")
        else:
            print(f"{audio_path} does not exist.")

        if os.path.exists(mp4_path):
            os.remove(mp4_path)
            print(f"{mp4_path} deleted successfully.")
        else:
            print(f"{mp4_path} does not exist.")

        print("Download is completed successfully")
    except Exception as e:
        bot.send_message(message.chat.id, 'Нажаль сталася помилка під час використання бота, '
                                          'перевірте посилання і спробуйте знову')
        print(e)


bot.polling(none_stop=True)
