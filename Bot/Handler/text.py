from Bot.bot import bot
from Bot.Keyboard import inline


@bot.message_handler(content_types=["text"])
def handler_message(message):
    if message.text == "Далее":
        text = "Четыре силы, некогда хранители гармонии, теперь объединились в жажде власти!\n\nВыберите класс:"
        markup = inline.Plot.introduction_class_selection()
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=markup)
