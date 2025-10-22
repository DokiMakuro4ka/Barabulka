from Bot.bot import bot
from Bot.Keyboard import inline


@bot.callback_query_handler(func=lambda call: True)
def handler_callback_query(call):
    if call.data == "class_selection":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Четыре силы, некогда хранители гармонии, теперь объединились в жажде власти!\n\nВыберите класс:"
        markup = inline.Plot.introduction_class_selection()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)


    elif call.data == "class_selection_fire":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Описание класса <Император Огня>"
        markup = inline.Plot.introduction_class_description_fire()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "class_selection_water":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Описание класса <Принцеса Воды>"
        markup = inline.Plot.introduction_class_description_water()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "class_selection_wind":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Описание класса <Царица Ветра>"
        markup = inline.Plot.introduction_class_description_wind()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "class_selection_land":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Описание класса <Царь Земли>"
        markup = inline.Plot.introduction_class_description_land()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)


    elif call.data == "select_class_fire":
        bot.send_message(chat_id=call.message.chat.id, text="В разработке")

    elif call.data == "select_class_water":
        bot.send_message(chat_id=call.message.chat.id, text="В разработке")

    elif call.data == "select_class_wind":
        bot.send_message(chat_id=call.message.chat.id, text="В разработке")

    elif call.data == "select_class_land":
        bot.send_message(chat_id=call.message.chat.id, text="В разработке")
