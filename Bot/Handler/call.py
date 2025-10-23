from Bot.bot import bot
from Bot.Keyboard import inline, reply
from DB.centre import User


@bot.callback_query_handler(func=lambda call: True)
def handler_callback_query(call):
    if call.data == "class_selection":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Четыре силы, некогда хранители гармонии, теперь объединились в жажде власти!\n\nВыберите класс:"
        markup = inline.Plot.introduction_class_selection()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)



    elif call.data == "class_selection_1":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Описание класса <Маг>.\n\nТут должен быть тект про описание класса и маленькая часть лора этого персонажа."
        markup = inline.Plot.introduction_class_description_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "class_selection_2":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Описание класса <Рыцарь>.\n\nТут должен быть тект про описание класса и маленькая часть лора этого персонажа."
        markup = inline.Plot.introduction_class_description_2()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "class_selection_3":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Описание класса <Лучник>.\n\nТут должен быть тект про описание класса и маленькая часть лора этого персонажа."
        markup = inline.Plot.introduction_class_description_3()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "class_selection_4":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Описание класса <Ассасин>.\n\nТут должен быть тект про описание класса и маленькая часть лора этого персонажа."
        markup = inline.Plot.introduction_class_description_4()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)



    elif call.data == "select_class_1":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Ты выбрал класс <Маг>.\n\nИди подойди к Капитану, он введёт тебя в курс дела."
        User.insert_user(user_id=call.from_user.id, class_id=1)
        markup = reply.Interface.interface_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "select_class_2":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Ты выбрал класс <Рыцарь>.\n\nИди подойди к Капитану, он введёт тебя в курс дела."
        User.insert_user(user_id=call.from_user.id, class_id=2)
        markup = reply.Interface.interface_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "select_class_3":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Ты выбрал класс <Лучник>.\n\nИди подойди к Капитану, он введёт тебя в курс дела."
        User.insert_user(user_id=call.from_user.id, class_id=3)
        markup = reply.Interface.interface_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)

    elif call.data == "select_class_4":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        text = "Ты выбрал класс <Ассасин>.\n\nИди подойди к Капитану, он введёт тебя в курс дела."
        User.insert_user(user_id=call.from_user.id, class_id=4)
        markup = reply.Interface.interface_1()
        bot.send_message(chat_id=call.message.chat.id, text=text, reply_markup=markup)
