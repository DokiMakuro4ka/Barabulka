from Bot.bot import bot

# Иницилизируем хендлеры, основной код
from Bot.Handler import call, command, text

print("----- БОТ ЗАПУЩЕН -----")
bot.infinity_polling()