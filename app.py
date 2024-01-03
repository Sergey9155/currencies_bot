import telebot
from extensions import APIException, Converter
from config import TOKEN, keys


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help_(message: telebot.types.Message):
    text = 'Чтобы начать работу, введите команды в следующем формате:\n <название валюты>  \
<в какую валюту перевести>  <количество переводимой валюты> \n Увидеть список всех доступных валют: /values '
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')

    try:
        if len(values) != 3:
            raise APIException('Передано не верное количество параметров')

        quote, base, amoute = values
        total_base = Converter.get_price(quote, base, amoute)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amoute} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)


bot.polling()
