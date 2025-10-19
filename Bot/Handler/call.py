from Bot.bot import bot
from Bot.Keyboard import inline


@bot.callback_query_handler(func=lambda call: True)
def handler_callback_query(call):
    if call.data == "Далее":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Четыре силы, некогда хранители гармонии, теперь объединились в жажде власти!\n\nВыберите класс:"
        markup = inline.Plot.introduction_2()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)


    elif call.data == "🔥 Император Огня 🔥":
        bot.send_message(chat_id=call.message.chat.id, text="В разработке")
    elif call.data == "💧 Принцеса Воды 💧":
        bot.send_message(chat_id=call.message.chat.id, text="В разработке")
    elif call.data == "💨 Царица Ветра 💨":
        bot.send_message(chat_id=call.message.chat.id, text="В разработке")
    elif call.data == "🪨 Царь Земли 🪨":
        bot.send_message(chat_id=call.message.chat.id, text="В разработке")
