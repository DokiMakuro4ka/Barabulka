from bot import bot
from Keyboard import reply


@bot.message_handler(content_types=["text"])
def handler_types_text(message):
    if message.text == "Далее":
        text = "Четыре силы, некогда хранители гармонии, теперь объединились в жажде власти!\n\nВыберите класс:"
        markup = reply.Plot.introduction_2()
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)
